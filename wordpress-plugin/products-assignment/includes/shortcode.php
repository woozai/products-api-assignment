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
	$product_request = products_assignment_get_product_request();
	$product_result  = products_assignment_get_products(
		$product_request['limit'],
		$product_request['skip'],
		$product_request['search_query']
	);
	$pagination      = products_assignment_build_pagination(
		$product_result['total'],
		$product_request['limit'],
		$product_request['current_page'],
		$product_request['search_query']
	);

	if ( '' === $product_result['error'] && $pagination['current_page'] !== $product_request['current_page'] ) {
		$product_result = products_assignment_get_products(
			$product_request['limit'],
			products_assignment_calculate_skip( $pagination['current_page'], $product_request['limit'] ),
			$product_request['search_query']
		);
	}

	if ( '' !== $product_result['error'] ) {
		return '<div class="products-assignment"><p>' . esc_html( $product_result['error'] ) . '</p></div>';
	}

	return '<div class="products-assignment"><p>' . esc_html__( 'Products loaded successfully.', 'products-assignment' ) . '</p></div>';
}
