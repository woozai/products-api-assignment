<?php
/**
 * Product normalization helpers for the Products Assignment plugin.
 *
 * @package ProductsAssignment
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Normalizes a list of raw DummyJSON product arrays.
 *
 * @param array $products Raw product arrays.
 * @return array
 */
function products_assignment_normalize_products( $products ) {
	if ( ! is_array( $products ) ) {
		return array();
	}

	return array_map( 'products_assignment_normalize_product', $products );
}

/**
 * Prepares one product for safe, predictable rendering.
 *
 * @param mixed $product Raw product data.
 * @return array
 */
function products_assignment_normalize_product( $product ) {
	if ( ! is_array( $product ) ) {
		$product = array();
	}

	$thumbnail = products_assignment_normalize_image_url( products_assignment_array_value( $product, 'thumbnail', '' ) );
	$images    = products_assignment_normalize_gallery_images( products_assignment_array_value( $product, 'images', array() ), $thumbnail );

	return array(
		'title'       => products_assignment_normalize_text( products_assignment_array_value( $product, 'title', '' ), __( 'Untitled product', 'products-assignment' ) ),
		'description' => products_assignment_normalize_text( products_assignment_array_value( $product, 'description', '' ), __( 'No description available.', 'products-assignment' ) ),
		'price'       => products_assignment_normalize_money( products_assignment_array_value( $product, 'price', null ) ),
		'rating'      => products_assignment_normalize_rating( products_assignment_array_value( $product, 'rating', null ) ),
		'stock'       => products_assignment_normalize_stock( products_assignment_array_value( $product, 'stock', null ) ),
		'brand'       => products_assignment_normalize_text( products_assignment_array_value( $product, 'brand', '' ), __( 'Unknown brand', 'products-assignment' ) ),
		'category'    => products_assignment_normalize_text( products_assignment_array_value( $product, 'category', '' ), __( 'Uncategorized', 'products-assignment' ) ),
		'thumbnail'   => $thumbnail,
		'images'      => $images,
	);
}

/**
 * Reads an array value without raising notices for missing fields.
 *
 * @param array  $product Product array.
 * @param string $key     Field name.
 * @param mixed  $default Fallback value.
 * @return mixed
 */
function products_assignment_array_value( $product, $key, $default ) {
	return array_key_exists( $key, $product ) ? $product[ $key ] : $default;
}

/**
 * Normalizes text fields with a readable fallback.
 *
 * @param mixed  $value    Raw text.
 * @param string $fallback Fallback text.
 * @return string
 */
function products_assignment_normalize_text( $value, $fallback ) {
	if ( ! is_scalar( $value ) ) {
		return $fallback;
	}

	$text = trim( wp_strip_all_tags( (string) $value ) );

	return '' === $text ? $fallback : $text;
}

/**
 * Normalizes a product price for display.
 *
 * @param mixed $value Raw price.
 * @return string
 */
function products_assignment_normalize_money( $value ) {
	if ( ! is_numeric( $value ) ) {
		return __( 'Price unavailable', 'products-assignment' );
	}

	return '$' . number_format_i18n( (float) $value, 2 );
}

/**
 * Normalizes a product rating for display.
 *
 * @param mixed $value Raw rating.
 * @return string
 */
function products_assignment_normalize_rating( $value ) {
	if ( ! is_numeric( $value ) ) {
		return __( 'No rating', 'products-assignment' );
	}

	return number_format_i18n( (float) $value, 1 );
}

/**
 * Normalizes product stock for display.
 *
 * @param mixed $value Raw stock.
 * @return string
 */
function products_assignment_normalize_stock( $value ) {
	if ( ! is_numeric( $value ) ) {
		return __( 'Stock unavailable', 'products-assignment' );
	}

	return number_format_i18n( max( 0, absint( $value ) ) );
}

/**
 * Keeps only safe image URLs.
 *
 * @param mixed $url Raw image URL.
 * @return string
 */
function products_assignment_normalize_image_url( $url ) {
	if ( ! is_scalar( $url ) ) {
		return '';
	}

	$url = esc_url_raw( trim( (string) $url ), array( 'http', 'https' ) );

	return '' === $url ? '' : $url;
}

/**
 * Normalizes gallery images and falls back to the thumbnail when needed.
 *
 * @param mixed  $images    Raw image list.
 * @param string $thumbnail Normalized thumbnail URL.
 * @return array
 */
function products_assignment_normalize_gallery_images( $images, $thumbnail ) {
	if ( ! is_array( $images ) ) {
		$images = array();
	}

	$normalized_images = array();

	foreach ( $images as $image_url ) {
		$normalized_url = products_assignment_normalize_image_url( $image_url );

		if ( '' !== $normalized_url && ! in_array( $normalized_url, $normalized_images, true ) ) {
			$normalized_images[] = $normalized_url;
		}

		if ( 3 === count( $normalized_images ) ) {
			break;
		}
	}

	if ( empty( $normalized_images ) && '' !== $thumbnail ) {
		$normalized_images[] = $thumbnail;
	}

	return $normalized_images;
}
