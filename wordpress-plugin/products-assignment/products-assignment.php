<?php
/**
 * Plugin Name: Products Assignment
 * Description: Bonus WordPress plugin for the DummyJSON products assignment.
 * Version: 1.0.0
 * Author: Lior
 * Text Domain: products-assignment
 *
 * @package ProductsAssignment
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'PRODUCTS_ASSIGNMENT_VERSION', '1.0.0' );
define( 'PRODUCTS_ASSIGNMENT_PATH', plugin_dir_path( __FILE__ ) );
define( 'PRODUCTS_ASSIGNMENT_URL', plugin_dir_url( __FILE__ ) );
define( 'PRODUCTS_ASSIGNMENT_SHORTCODE', 'products_assignment' );
define( 'PRODUCTS_ASSIGNMENT_PAGE_TITLE', 'Compare Assignment' );
define( 'PRODUCTS_ASSIGNMENT_PAGE_OPTION', 'products_assignment_page_id' );
define( 'PRODUCTS_ASSIGNMENT_PAGE_SIZE', 10 );

require_once PRODUCTS_ASSIGNMENT_PATH . 'includes/activation.php';
require_once PRODUCTS_ASSIGNMENT_PATH . 'includes/products.php';
require_once PRODUCTS_ASSIGNMENT_PATH . 'includes/dummyjson-api.php';
require_once PRODUCTS_ASSIGNMENT_PATH . 'includes/shortcode.php';

register_activation_hook( __FILE__, 'products_assignment_activate' );
register_deactivation_hook( __FILE__, 'products_assignment_deactivate' );

add_action( 'init', 'products_assignment_register_shortcode' );
