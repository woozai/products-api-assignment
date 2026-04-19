const openGalleryClass = 'gallery-row';

function parseProductImages(galleryButton) {
  try {
    const productImages = JSON.parse(galleryButton.dataset.productImages || '[]');
    return productImages.slice(0, 3);
  } catch {
    return [];
  }
}

function closeOpenGallery() {
  const openGalleryRow = document.querySelector(`.${openGalleryClass}`);

  if (openGalleryRow) {
    openGalleryRow.remove();
  }
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
  galleryContent.className = 'gallery-content';

  if (productImages.length === 0) {
    galleryContent.textContent = 'No gallery images are available for this product.';
    return galleryContent;
  }

  productImages.forEach((imageUrl, imageIndex) => {
    galleryContent.appendChild(createGalleryImage(imageUrl, productTitle, imageIndex));
  });

  return galleryContent;
}

function createGalleryRow(galleryButton) {
  const productTitle = galleryButton.dataset.productTitle || 'Product';
  const productImages = parseProductImages(galleryButton);
  const galleryRow = document.createElement('tr');
  const galleryCell = document.createElement('td');

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
  const isCurrentGalleryOpen =
    nextRow?.classList.contains(openGalleryClass) &&
    nextRow.dataset.productTitle === galleryButton.dataset.productTitle;

  closeOpenGallery();

  if (isCurrentGalleryOpen) {
    return;
  }

  productRow.insertAdjacentElement('afterend', createGalleryRow(galleryButton));
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.gallery-button').forEach((galleryButton) => {
    galleryButton.addEventListener('click', () => toggleProductGallery(galleryButton));
  });
});
