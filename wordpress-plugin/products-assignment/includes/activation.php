<?php
/**
 * Activation and deactivation hooks for the Products Assignment plugin.
 *
 * @package ProductsAssignment
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Runs when the plugin is activated.
 */
function products_assignment_activate() {
	$page_id = products_assignment_find_page_id();

	if ( 0 === $page_id ) {
		$page_id = products_assignment_create_page();
	}

	if ( $page_id > 0 ) {
		update_option( PRODUCTS_ASSIGNMENT_PAGE_OPTION, $page_id );
	}
}

/**
 * Runs when the plugin is deactivated.
 */
function products_assignment_deactivate() {
	// Keep plugin data in place so reactivation can reuse the same page safely.
}

/**
 * Finds an existing assignment page by title.
 *
 * @return int
 */
function products_assignment_find_page_id() {
	$stored_page_id = absint( get_option( PRODUCTS_ASSIGNMENT_PAGE_OPTION, 0 ) );

	if ( $stored_page_id > 0 && 'page' === get_post_type( $stored_page_id ) ) {
		return $stored_page_id;
	}

	// Reuse a matching page instead of creating duplicate assignment pages.
	$pages = get_posts(
		array(
			'post_type'              => 'page',
			'post_status'            => 'any',
			'title'                  => PRODUCTS_ASSIGNMENT_PAGE_TITLE,
			'posts_per_page'         => 1,
			'fields'                 => 'ids',
			'no_found_rows'          => true,
			'update_post_meta_cache' => false,
			'update_post_term_cache' => false,
		)
	);

	if ( ! empty( $pages ) ) {
		return absint( $pages[0] );
	}

	return 0;
}

/**
 * Creates the assignment page with the shortcode as its content.
 *
 * @return int
 */
function products_assignment_create_page() {
	$page_id = wp_insert_post(
		array(
			'post_title'   => PRODUCTS_ASSIGNMENT_PAGE_TITLE,
			'post_content' => '[' . PRODUCTS_ASSIGNMENT_SHORTCODE . ']',
			'post_status'  => 'publish',
			'post_type'    => 'page',
		),
		true
	);

	if ( is_wp_error( $page_id ) ) {
		return 0;
	}

	return absint( $page_id );
}
