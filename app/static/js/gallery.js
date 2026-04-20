const openGalleryClass = 'gallery-row';
const activeGalleryButtonClass = 'gallery-button-active';

function resetGalleryButtons() {
  document.querySelectorAll(`.${activeGalleryButtonClass}`).forEach((galleryButton) => {
    galleryButton.classList.remove(activeGalleryButtonClass);
    galleryButton.setAttribute('aria-expanded', 'false');
    galleryButton.setAttribute(
      'aria-label',
      `View gallery for ${galleryButton.dataset.productTitle || 'product'}`,
    );
  });
}

function parseProductImages(galleryButton) {
  try {
    // Images are rendered by Jinja so the browser never calls DummyJSON directly.
    const productImages = JSON.parse(galleryButton.dataset.productImages || '[]');
    // The assignment asks for up to 3 gallery images.
    return productImages.slice(0, 3);
  } catch {
    // Bad data should show the fallback message instead of breaking the click.
    return [];
  }
}

function closeOpenGallery() {
  const openGalleryRow = document.querySelector(`.${openGalleryClass}`);

  // Removing the existing row keeps only one gallery open at a time.
  if (openGalleryRow) {
    openGalleryRow.remove();
  }

  resetGalleryButtons();
}

function createGalleryImage(imageUrl, productTitle, imageIndex) {
  const galleryImage = document.createElement('img');
  galleryImage.className = 'gallery-image';
  galleryImage.src = imageUrl;
  galleryImage.alt = `${productTitle} gallery image ${imageIndex + 1}`;

  return galleryImage;
}

function createGalleryContent(productTitle, productImages) {
  const galleryContent = document.createElement('div');
  const galleryHeading = document.createElement('h2');
  const galleryImages = document.createElement('div');

  galleryContent.className = 'gallery-content';
  galleryHeading.className = 'gallery-heading';
  galleryHeading.textContent = `Images for ${productTitle}`;
  galleryImages.className = 'gallery-images';
  galleryContent.appendChild(galleryHeading);

  // Some products may not have extra images beyond the thumbnail.
  if (productImages.length === 0) {
    galleryImages.textContent = 'No gallery images are available for this product.';
    galleryContent.appendChild(galleryImages);
    return galleryContent;
  }

  productImages.forEach((imageUrl, imageIndex) => {
    galleryImages.appendChild(createGalleryImage(imageUrl, productTitle, imageIndex));
  });
  galleryContent.appendChild(galleryImages);

  return galleryContent;
}

function createGalleryRow(galleryButton) {
  const productTitle = galleryButton.dataset.productTitle || 'Product';
  const productImages = parseProductImages(galleryButton);
  const galleryRow = document.createElement('tr');
  const galleryCell = document.createElement('td');

  // The inserted row sits directly below the clicked product row.
  galleryRow.className = openGalleryClass;
  galleryRow.dataset.productTitle = productTitle;
  galleryCell.colSpan = galleryButton.closest('tr').children.length;
  galleryCell.appendChild(createGalleryContent(productTitle, productImages));
  galleryRow.appendChild(galleryCell);

  return galleryRow;
}

function toggleProductGallery(galleryButton) {
  const productRow = galleryButton.closest('tr');
  const nextRow = productRow.nextElementSibling;

  // Only one gallery stays open, and clicking the same product closes it.
  const isCurrentGalleryOpen =
    nextRow?.classList.contains(openGalleryClass) &&
    nextRow.dataset.productTitle === galleryButton.dataset.productTitle;

  closeOpenGallery();

  if (isCurrentGalleryOpen) {
    return;
  }

  productRow.insertAdjacentElement('afterend', createGalleryRow(galleryButton));
  galleryButton.classList.add(activeGalleryButtonClass);
  galleryButton.setAttribute('aria-expanded', 'true');
  galleryButton.setAttribute(
    'aria-label',
    `Hide gallery for ${galleryButton.dataset.productTitle || 'product'}`,
  );
}

document.addEventListener('DOMContentLoaded', () => {
  // Attach listeners after the table has been rendered by Flask/Jinja.
  document.querySelectorAll('.gallery-button').forEach((galleryButton) => {
    galleryButton.setAttribute('aria-expanded', 'false');
    galleryButton.addEventListener('click', () => toggleProductGallery(galleryButton));
  });
});
