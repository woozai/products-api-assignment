<?php
/**
 * Shortcode registration for the Products Assignment plugin.
 *
 * @package ProductsAssignment
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Registers the products assignment shortcode.
 */
function products_assignment_register_shortcode() {
	add_shortcode( PRODUCTS_ASSIGNMENT_SHORTCODE, 'products_assignment_render_shortcode' );
}

/**
 * Renders a temporary shortcode placeholder until the product table UI is built.
 *
 * @return string
 */
function products_assignment_render_shortcode() {
	$product_result = products_assignment_get_products( PRODUCTS_ASSIGNMENT_PAGE_SIZE, 0 );

	if ( '' !== $product_result['error'] ) {
		return '<div class="products-assignment"><p>' . esc_html( $product_result['error'] ) . '</p></div>';
	}

	return '<div class="products-assignment"><p>' . esc_html__( 'Products loaded successfully.', 'products-assignment' ) . '</p></div>';
}
