(function () {
	'use strict';

	var galleryRowClass = 'products-assignment__gallery-row';
	var galleryButtonSelector = '.products-assignment__gallery-button';

	function closeAllGalleries() {
		var openButtons = document.querySelectorAll(galleryButtonSelector + '[aria-expanded="true"]');
		var openGalleryRows = document.querySelectorAll('.' + galleryRowClass);

		openGalleryRows.forEach(function (openGalleryRow) {
			openGalleryRow.remove();
		});

		openButtons.forEach(function (openButton) {
			openButton.setAttribute('aria-expanded', 'false');
		});
	}

	function getButtonImages(button) {
		var parsedImages;

		try {
			parsedImages = JSON.parse(button.dataset.images || '[]');
		} catch (error) {
			parsedImages = [];
		}

		if (!Array.isArray(parsedImages)) {
			return [];
		}

		return parsedImages
			.filter(function (imageUrl) {
				return typeof imageUrl === 'string' && /^https?:\/\//i.test(imageUrl);
			})
			.slice(0, 3);
	}

	function createGalleryContent(button) {
		var galleryContent = document.createElement('div');
		var images = getButtonImages(button);
		var productTitle = button.dataset.productTitle || 'Product image';

		galleryContent.className = 'products-assignment__gallery';

		if (images.length === 0) {
			galleryContent.textContent = 'No gallery images available.';
			return galleryContent;
		}

		images.forEach(function (imageUrl, index) {
			var image = document.createElement('img');

			image.className = 'products-assignment__gallery-image';
			image.src = imageUrl;
			image.alt = productTitle + ' gallery image ' + (index + 1);
			image.loading = 'lazy';
			galleryContent.appendChild(image);
		});

		return galleryContent;
	}

	function createGalleryRow(productRow, button) {
		var galleryRow = document.createElement('tr');
		var galleryCell = document.createElement('td');

		galleryRow.className = galleryRowClass;
		galleryCell.colSpan = productRow.cells.length;
		galleryCell.appendChild(createGalleryContent(button));
		galleryRow.appendChild(galleryCell);

		return galleryRow;
	}

	function handleGalleryClick(event) {
		var button;
		var productRow;
		var table;
		var galleryRow;

		if (!event.target || typeof event.target.closest !== 'function') {
			return;
		}

		button = event.target.closest(galleryButtonSelector);

		if (!button) {
			return;
		}

		productRow = button.closest('tr');
		table = button.closest('table');

		if (!productRow || !table) {
			return;
		}

		if (button.getAttribute('aria-expanded') === 'true') {
			closeAllGalleries();
			return;
		}

		closeAllGalleries();
		galleryRow = createGalleryRow(productRow, button);
		productRow.insertAdjacentElement('afterend', galleryRow);
		button.setAttribute('aria-expanded', 'true');
	}

	document.addEventListener('click', handleGalleryClick);
}());
