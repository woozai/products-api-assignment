<?php
/**
 * DummyJSON API helpers for the Products Assignment plugin.
 *
 * @package ProductsAssignment
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'PRODUCTS_ASSIGNMENT_DUMMYJSON_BASE_URL', 'https://dummyjson.com' );
define( 'PRODUCTS_ASSIGNMENT_DUMMYJSON_TIMEOUT', 5 );

/**
 * Fetches products from DummyJSON using either the list or search endpoint.
 *
 * @param int    $limit        Number of products to request.
 * @param int    $skip         Number of products to skip.
 * @param string $search_query Optional product search query.
 * @return array
 */
function products_assignment_get_products( $limit = PRODUCTS_ASSIGNMENT_PAGE_SIZE, $skip = 0, $search_query = '' ) {
	$limit        = max( 1, absint( $limit ) );
	$skip         = max( 0, absint( $skip ) );
	$search_query = sanitize_text_field( $search_query );
	$url          = products_assignment_build_products_url( $limit, $skip, $search_query );

	$response = wp_remote_get(
		$url,
		array(
			'timeout' => PRODUCTS_ASSIGNMENT_DUMMYJSON_TIMEOUT,
		)
	);

	if ( is_wp_error( $response ) ) {
		return products_assignment_product_result_with_error( $limit, $skip );
	}

	$status_code = wp_remote_retrieve_response_code( $response );

	if ( 200 !== $status_code ) {
		return products_assignment_product_result_with_error( $limit, $skip );
	}

	$decoded_response = json_decode( wp_remote_retrieve_body( $response ), true );

	if ( JSON_ERROR_NONE !== json_last_error() || ! products_assignment_is_valid_product_response( $decoded_response ) ) {
		return products_assignment_product_result_with_error( $limit, $skip );
	}

	return array(
		'products' => $decoded_response['products'],
		'total'    => absint( $decoded_response['total'] ),
		'skip'     => absint( $decoded_response['skip'] ),
		'limit'    => absint( $decoded_response['limit'] ),
		'error'    => '',
	);
}

/**
 * Builds the correct DummyJSON endpoint URL for listing or searching products.
 *
 * @param int    $limit        Number of products to request.
 * @param int    $skip         Number of products to skip.
 * @param string $search_query Optional product search query.
 * @return string
 */
function products_assignment_build_products_url( $limit, $skip, $search_query ) {
	$has_search_query = '' !== trim( $search_query );
	$endpoint         = $has_search_query ? '/products/search' : '/products';
	$query_args       = array(
		'limit' => $limit,
		'skip'  => $skip,
	);

	if ( $has_search_query ) {
		$query_args['q'] = $search_query;
	}

	return add_query_arg(
		$query_args,
		PRODUCTS_ASSIGNMENT_DUMMYJSON_BASE_URL . $endpoint
	);
}

/**
 * Checks that the decoded API response has the shape the shortcode expects.
 *
 * @param mixed $decoded_response Decoded JSON response.
 * @return bool
 */
function products_assignment_is_valid_product_response( $decoded_response ) {
	return is_array( $decoded_response )
		&& isset( $decoded_response['products'], $decoded_response['total'], $decoded_response['skip'], $decoded_response['limit'] )
		&& is_array( $decoded_response['products'] )
		&& is_numeric( $decoded_response['total'] )
		&& is_numeric( $decoded_response['skip'] )
		&& is_numeric( $decoded_response['limit'] );
}

/**
 * Returns a predictable failed result without exposing remote error details.
 *
 * @param int $limit Number of products requested.
 * @param int $skip  Number of products skipped.
 * @return array
 */
function products_assignment_product_result_with_error( $limit, $skip ) {
	return array(
		'products' => array(),
		'total'    => 0,
		'skip'     => $skip,
		'limit'    => $limit,
		'error'    => __( 'Products are temporarily unavailable. Please try again soon.', 'products-assignment' ),
	);
}
