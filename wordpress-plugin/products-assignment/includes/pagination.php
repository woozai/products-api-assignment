<?php
/**
 * Request parsing and pagination helpers for the Products Assignment plugin.
 *
 * @package ProductsAssignment
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Reads the current shortcode request values from the URL.
 *
 * @param int $limit Number of products per page.
 * @return array
 */
function products_assignment_get_product_request( $limit = PRODUCTS_ASSIGNMENT_PAGE_SIZE ) {
	$current_page = products_assignment_get_current_page_number();
	$limit        = max( 1, absint( $limit ) );

	return array(
		'search_query' => products_assignment_get_current_search_query(),
		'current_page' => $current_page,
		'limit'        => $limit,
		'skip'         => products_assignment_calculate_skip( $current_page, $limit ),
	);
}

/**
 * Reads and sanitizes the product search query from the URL.
 *
 * @return string
 */
function products_assignment_get_current_search_query() {
	if ( ! isset( $_GET['q'] ) || is_array( $_GET['q'] ) ) {
		return '';
	}

	return trim( sanitize_text_field( wp_unslash( $_GET['q'] ) ) );
}

/**
 * Reads the current product page number from the URL.
 *
 * @return int
 */
function products_assignment_get_current_page_number() {
	if ( ! isset( $_GET['product_page'] ) || is_array( $_GET['product_page'] ) ) {
		return 1;
	}

	$page_value = trim( (string) wp_unslash( $_GET['product_page'] ) );

	if ( ! ctype_digit( $page_value ) ) {
		return 1;
	}

	$page_number = absint( $page_value );

	return $page_number < 1 ? 1 : $page_number;
}

/**
 * Converts a page number into a DummyJSON skip value.
 *
 * @param int $page_number Current page number.
 * @param int $limit       Number of products per page.
 * @return int
 */
function products_assignment_calculate_skip( $page_number, $limit ) {
	$page_number = max( 1, absint( $page_number ) );
	$limit       = max( 1, absint( $limit ) );

	return ( $page_number - 1 ) * $limit;
}

/**
 * Builds pagination values and links after the API total is known.
 *
 * @param int    $total        Total matching products.
 * @param int    $limit        Number of products per page.
 * @param int    $current_page Current page number.
 * @param string $search_query Active search query.
 * @return array
 */
function products_assignment_build_pagination( $total, $limit, $current_page, $search_query = '' ) {
	$total        = max( 0, absint( $total ) );
	$limit        = max( 1, absint( $limit ) );
	$total_pages  = max( 1, (int) ceil( $total / $limit ) );
	$current_page = min( max( 1, absint( $current_page ) ), $total_pages );
	$has_previous = $current_page > 1;
	$has_next     = $current_page < $total_pages;

	return array(
		'current_page' => $current_page,
		'total_pages'  => $total_pages,
		'previous_url' => $has_previous ? products_assignment_build_page_url( $current_page - 1, $search_query ) : '',
		'next_url'     => $has_next ? products_assignment_build_page_url( $current_page + 1, $search_query ) : '',
		'page_urls'    => products_assignment_build_page_urls( $total_pages, $search_query ),
		'has_previous' => $has_previous,
		'has_next'     => $has_next,
	);
}

/**
 * Builds links for each available product page.
 *
 * @param int    $total_pages  Total number of pages.
 * @param string $search_query Active search query.
 * @return array
 */
function products_assignment_build_page_urls( $total_pages, $search_query = '' ) {
	$page_urls = array();

	for ( $page_number = 1; $page_number <= $total_pages; $page_number++ ) {
		$page_urls[ $page_number ] = products_assignment_build_page_url( $page_number, $search_query );
	}

	return $page_urls;
}

/**
 * Builds one pagination URL while preserving the active search query.
 *
 * @param int    $page_number  Page number.
 * @param string $search_query Active search query.
 * @return string
 */
function products_assignment_build_page_url( $page_number, $search_query = '' ) {
	$query_args = array(
		'product_page' => max( 1, absint( $page_number ) ),
	);

	$search_query = trim( sanitize_text_field( $search_query ) );

	if ( '' !== $search_query ) {
		$query_args['q'] = $search_query;
	}

	return add_query_arg(
		$query_args,
		remove_query_arg( array( 'product_page', 'q' ) )
	);
}
