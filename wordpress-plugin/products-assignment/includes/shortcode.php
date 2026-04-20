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
 * Renders the products assignment shortcode.
 *
 * @return string
 */
function products_assignment_render_shortcode() {
	products_assignment_enqueue_assets();

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

	return products_assignment_render_template(
		'products-table.php',
		array(
			'products'       => $product_result['products'],
			'error'          => $product_result['error'],
			'search_query'   => $product_request['search_query'],
			'pagination'     => $pagination,
			'product_result' => $product_result,
		)
	);
}

/**
 * Renders a plugin template with prepared variables.
 *
 * @param string $template_name Template file name.
 * @param array  $variables     Variables for the template.
 * @return string
 */
function products_assignment_render_template( $template_name, $variables = array() ) {
	$template_path = PRODUCTS_ASSIGNMENT_PATH . 'templates/' . $template_name;

	if ( ! file_exists( $template_path ) ) {
		return '';
	}

	extract( $variables, EXTR_SKIP );

	ob_start();
	include $template_path;
	return ob_get_clean();
}
