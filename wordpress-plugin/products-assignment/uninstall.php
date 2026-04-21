<?php
/**
 * Uninstall cleanup for the Products Assignment plugin.
 *
 * @package ProductsAssignment
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
	exit;
}

delete_option( 'products_assignment_page_id' );
