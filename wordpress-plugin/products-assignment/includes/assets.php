<?php
/**
 * Asset loading helpers for the Products Assignment plugin.
 *
 * @package ProductsAssignment
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Enqueues plugin assets only when the shortcode renders.
 */
function products_assignment_enqueue_assets() {
	wp_enqueue_style(
		'products-assignment',
		PRODUCTS_ASSIGNMENT_URL . 'assets/css/products-assignment.css',
		array(),
		PRODUCTS_ASSIGNMENT_VERSION
	);

	wp_enqueue_script(
		'products-assignment-gallery',
		PRODUCTS_ASSIGNMENT_URL . 'assets/js/gallery.js',
		array(),
		PRODUCTS_ASSIGNMENT_VERSION,
		true
	);
}
