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
	// Page creation belongs in Phase 2. Keep activation safe for the shell.
}

/**
 * Runs when the plugin is deactivated.
 */
function products_assignment_deactivate() {
	// No cleanup is needed yet because Phase 1 does not create persistent data.
}
