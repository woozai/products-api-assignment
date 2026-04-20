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
 * Renders a temporary shortcode placeholder until the product table is built.
 *
 * @return string
 */
function products_assignment_render_shortcode() {
	return '<div class="products-assignment"><p>' . esc_html__( 'Products assignment plugin is ready.', 'products-assignment' ) . '</p></div>';
}
