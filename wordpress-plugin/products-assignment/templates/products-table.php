<?php
/**
 * Products assignment shortcode template.
 *
 * @package ProductsAssignment
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
?>

<div class="products-assignment">
	<form class="products-assignment__search" method="get">
		<label for="products-assignment-search"><?php echo esc_html__( 'Search products', 'products-assignment' ); ?></label>
		<input id="products-assignment-search" type="search" name="q" value="<?php echo esc_attr( $search_query ); ?>">
		<button type="submit"><?php echo esc_html__( 'Search', 'products-assignment' ); ?></button>
	</form>

	<?php if ( '' !== $error ) : ?>
		<p class="products-assignment__message"><?php echo esc_html( $error ); ?></p>
	<?php elseif ( empty( $products ) ) : ?>
		<p class="products-assignment__message"><?php echo esc_html__( 'No products found.', 'products-assignment' ); ?></p>
	<?php else : ?>
		<table class="products-assignment__table">
			<thead>
				<tr>
					<th scope="col"><?php echo esc_html__( 'Title', 'products-assignment' ); ?></th>
					<th scope="col"><?php echo esc_html__( 'Description', 'products-assignment' ); ?></th>
					<th scope="col"><?php echo esc_html__( 'Price', 'products-assignment' ); ?></th>
					<th scope="col"><?php echo esc_html__( 'Rating', 'products-assignment' ); ?></th>
					<th scope="col"><?php echo esc_html__( 'Stock', 'products-assignment' ); ?></th>
					<th scope="col"><?php echo esc_html__( 'Brand', 'products-assignment' ); ?></th>
					<th scope="col"><?php echo esc_html__( 'Category', 'products-assignment' ); ?></th>
					<th scope="col"><?php echo esc_html__( 'Thumbnail', 'products-assignment' ); ?></th>
				</tr>
			</thead>
			<tbody>
				<?php foreach ( $products as $product ) : ?>
					<tr>
						<td><?php echo esc_html( $product['title'] ); ?></td>
						<td><?php echo esc_html( $product['description'] ); ?></td>
						<td><?php echo esc_html( $product['price'] ); ?></td>
						<td><?php echo esc_html( $product['rating'] ); ?></td>
						<td><?php echo esc_html( $product['stock'] ); ?></td>
						<td><?php echo esc_html( $product['brand'] ); ?></td>
						<td><?php echo esc_html( $product['category'] ); ?></td>
						<td>
							<?php if ( '' !== $product['thumbnail'] ) : ?>
								<img class="products-assignment__thumbnail" src="<?php echo esc_url( $product['thumbnail'] ); ?>" alt="<?php echo esc_attr( $product['title'] ); ?>">
							<?php else : ?>
								<?php echo esc_html__( 'No image', 'products-assignment' ); ?>
							<?php endif; ?>
						</td>
					</tr>
				<?php endforeach; ?>
			</tbody>
		</table>
	<?php endif; ?>

	<?php if ( $pagination['total_pages'] > 1 ) : ?>
		<nav class="products-assignment__pagination" aria-label="<?php echo esc_attr__( 'Product pages', 'products-assignment' ); ?>">
			<?php if ( $pagination['has_previous'] ) : ?>
				<a href="<?php echo esc_url( $pagination['previous_url'] ); ?>"><?php echo esc_html__( 'Previous', 'products-assignment' ); ?></a>
			<?php endif; ?>

			<span>
				<?php
				echo esc_html(
					sprintf(
						/* translators: 1: current page number, 2: total pages. */
						__( 'Page %1$d of %2$d', 'products-assignment' ),
						$pagination['current_page'],
						$pagination['total_pages']
					)
				);
				?>
			</span>

			<?php if ( $pagination['has_next'] ) : ?>
				<a href="<?php echo esc_url( $pagination['next_url'] ); ?>"><?php echo esc_html__( 'Next', 'products-assignment' ); ?></a>
			<?php endif; ?>
		</nav>
	<?php endif; ?>
</div>
