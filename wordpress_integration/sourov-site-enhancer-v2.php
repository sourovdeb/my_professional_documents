<?php
/**
 * Plugin Name: Sourov Site Enhancer
 * Plugin URI: https://sourovdeb.com
 * Description: ELT series navigation, YouTube/podcast embedding per post, related articles, YouTube channel CTA, sidebar widget, and shortcodes.
 * Version: 2.0.0
 * Author: Sourov DEB
 */

if ( ! defined( 'ABSPATH' ) ) exit;

define( 'SSD_YT_CHANNEL_URL',  'https://www.youtube.com/channel/UC1rs5aY7YdFiADKkhOMPCvQ' );
define( 'SSD_YT_CHANNEL_NAME', 'Treasure Hunters Digital' );

class Sourov_Site_Enhancer {

	private static $day_map = null;

	public function __construct() {
		add_action( 'wp_head',        [ $this, 'styles'        ], 99 );
		add_filter( 'the_content',    [ $this, 'media_embeds'  ], 10 );
		add_filter( 'the_content',    [ $this, 'series_nav'    ], 20 );
		add_filter( 'the_content',    [ $this, 'youtube_cta'   ], 22 );
		add_filter( 'the_content',    [ $this, 'related_posts' ], 30 );
		add_action( 'add_meta_boxes', [ $this, 'meta_boxes'    ] );
		add_action( 'save_post',      [ $this, 'save_meta'     ] );
		add_action( 'widgets_init',   [ $this, 'register_widget'] );

		// Shortcodes
		add_shortcode( 'sourov_youtube', [ $this, 'sc_youtube' ] );
		add_shortcode( 'sourov_podcast', [ $this, 'sc_podcast' ] );
	}

	// ── Styles ─────────────────────────────────────────────────────────────────
	public function styles() {
		echo '<style id="ssd-styles">
.ssd-nav{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5em;margin:1.5em 0;padding:.85em 1.1em;background:#eef4fb;border-left:4px solid #0073aa;font-size:.88em;line-height:1.4;border-radius:0 4px 4px 0}
.ssd-nav a{text-decoration:none;max-width:42%}
.ssd-nav .ssd-p{color:#0055a4;font-weight:600}
.ssd-nav .ssd-n{color:#0055a4;font-weight:600;text-align:right}
.ssd-nav .ssd-i{color:#555;white-space:nowrap;font-size:.9em}
.ssd-yt-wrap{position:relative;padding-bottom:56.25%;height:0;overflow:hidden;margin:0 0 1.5em;border-radius:8px;background:#000}
.ssd-yt-wrap iframe{position:absolute;top:0;left:0;width:100%;height:100%;border:0}
.ssd-pod{margin:0 0 1.25em;padding:.75em 1.1em;background:#1a1a2e;border-radius:6px;color:#e0e0e0;font-size:.9em}
.ssd-pod a{color:#a78bfa;text-decoration:none;font-weight:600}
.ssd-yt-cta{display:flex;align-items:center;gap:14px;flex-wrap:wrap;background:#fff5f5;border:1px solid #fed7d7;border-radius:8px;padding:14px 18px;margin:28px 0}
.ssd-yt-cta strong{display:block;font-size:14px;color:#2d3748;margin-bottom:3px}
.ssd-yt-cta a{color:#cc0000;text-decoration:none;font-size:13px;font-weight:500}
.ssd-related-grid{border-top:2px solid #e2e8f0;margin-top:40px;padding-top:24px}
.ssd-related-grid h3{font-size:17px;font-weight:600;color:#2d3748;margin:0 0 16px}
.ssd-related-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:14px}
.ssd-related-card{background:#f7fafc;border-radius:8px;padding:14px 16px;border:1px solid #edf2f7}
.ssd-related-card .ssd-cat{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:#718096;display:block;margin-bottom:5px}
.ssd-related-card a{color:#2b6cb0;text-decoration:none;font-size:14px;font-weight:500;line-height:1.45;display:block}
.ssd-related-card a:hover{text-decoration:underline}
.ssd-related-card time{font-size:11px;color:#a0aec0;display:block;margin-top:8px}
.ssd-yt-embed{margin:24px 0;border-radius:10px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.12)}
.ssd-yt-embed .ssd-yt-wrap{margin:0;border-radius:0}
.ssd-audio{background:#f7fafc;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px;margin:20px 0}
.ssd-audio p{font-size:13px;font-weight:600;color:#4a5568;margin:0 0 8px}
.ssd-audio audio{width:100%;display:block}
.ssd-yt-widget{text-align:center;padding:10px 0}
.ssd-yt-widget a{display:inline-flex;align-items:center;gap:8px;background:#cc0000;color:#fff;text-decoration:none;padding:9px 18px;border-radius:4px;font-size:14px;font-weight:600;line-height:1}
.ssd-yt-widget p{font-size:12px;color:#718096;margin:8px 0 0}
@media(max-width:600px){.ssd-nav a{max-width:100%}.ssd-nav .ssd-i{order:-1;width:100%;text-align:center}}
</style>' . "\n";
	}

	// ── Day number / label ─────────────────────────────────────────────────────
	private function day_num( $title ) {
		$t = strip_tags( $title );
		if ( preg_match( '/\bDay\s+(\d+)\b/i',     $t, $m ) ) return (int) $m[1];
		if ( preg_match( '/\b(\d+)\s+of\s+60\b/i', $t, $m ) ) return (int) $m[1];
		return null;
	}

	private function day_label( $title ) {
		$t = strip_tags( $title );
		$t = preg_replace( '/[\x{1F000}-\x{1FFFF}\x{2600}-\x{27BF}]/u', '', $t );
		$t = preg_replace( '/^\s*Day\s+\d+\s*(?:of\s*60)?\s*[:\-·|]+\s*/i', '', $t );
		$t = preg_replace( '/^\s*\d+\s+of\s+60\s*[:\-·|]+\s*/i', '', $t );
		return trim( $t );
	}

	private function build_day_map() {
		if ( self::$day_map !== null ) return self::$day_map;
		$posts = get_posts( [
			'category'    => 9,
			'numberposts' => -1,
			'post_status' => 'publish',
			'orderby'     => 'ID',
		] );
		self::$day_map = [];
		foreach ( $posts as $p ) {
			$d = $this->day_num( $p->post_title );
			if ( $d ) self::$day_map[ $d ] = $p;
		}
		return self::$day_map;
	}

	// ── ELT Series Navigation ──────────────────────────────────────────────────
	public function series_nav( $content ) {
		if ( ! is_single() ) return $content;
		global $post;

		$cats = (array) wp_get_post_categories( $post->ID );
		if ( ! in_array( 9, $cats, true ) ) return $content;

		$day = $this->day_num( $post->post_title );
		if ( ! $day ) return $content;

		$map  = $this->build_day_map();
		$prev = $map[ $day - 1 ] ?? null;
		$next = $map[ $day + 1 ] ?? null;

		$nav  = '<nav class="ssd-nav" aria-label="ELT Masterclass series navigation">';
		$nav .= $prev
			? '<a class="ssd-p" href="' . esc_url( get_permalink( $prev->ID ) ) . '">&#8592; Day ' . ( $day - 1 ) . ': ' . esc_html( mb_strimwidth( $this->day_label( $prev->post_title ), 0, 44, '&hellip;' ) ) . '</a>'
			: '<span></span>';
		$nav .= '<a class="ssd-i" href="' . esc_url( home_url( '/elt-masterclass/' ) ) . '">&#128203;&nbsp;Series&nbsp;Index</a>';
		$nav .= $next
			? '<a class="ssd-n" href="' . esc_url( get_permalink( $next->ID ) ) . '">Day ' . ( $day + 1 ) . ': ' . esc_html( mb_strimwidth( $this->day_label( $next->post_title ), 0, 44, '&hellip;' ) ) . ' &#8594;</a>'
			: '<span></span>';
		$nav .= '</nav>';

		return $nav . $content . $nav;
	}

	// ── YouTube Channel CTA (all content-category posts, no specific video set) ──
	public function youtube_cta( $content ) {
		if ( ! is_singular( 'post' ) || ! in_the_loop() ) return $content;
		global $post;

		// Don't show if a specific YouTube video is set for this post
		if ( get_post_meta( $post->ID, '_ssd_yt', true ) ) return $content;

		$cats      = (array) wp_get_post_categories( $post->ID );
		$show_cats = [ 9, 581, 582 ]; // English Teaching, Philosophy, Mental Health
		if ( empty( array_intersect( $cats, $show_cats ) ) ) return $content;

		$yt_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="#CC0000" style="flex-shrink:0"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>';

		return $content . '<div class="ssd-yt-cta">' . $yt_icon . '<div><strong>Prefer watching over reading?</strong><a href="' . esc_url( SSD_YT_CHANNEL_URL ) . '" target="_blank" rel="noopener noreferrer">Visit ' . esc_html( SSD_YT_CHANNEL_NAME ) . ' on YouTube &#8594;</a></div></div>';
	}

	// ── YouTube / Podcast meta boxes ───────────────────────────────────────────
	public function meta_boxes() {
		add_meta_box(
			'ssd_media',
			'&#128250; YouTube &nbsp;&#183;&nbsp; &#127897; Podcast',
			[ $this, 'meta_box_html' ],
			'post', 'side', 'high'
		);
	}

	public function meta_box_html( $post ) {
		$yt  = get_post_meta( $post->ID, '_ssd_yt',  true );
		$pod = get_post_meta( $post->ID, '_ssd_pod', true );
		wp_nonce_field( 'ssd_save_media', 'ssd_media_nonce' );
		echo '<p style="margin:0 0 3px;font-size:11px;font-weight:600;color:#444">YouTube URL</p>';
		echo '<input type="url" name="ssd_yt"  value="' . esc_attr( $yt )  . '" placeholder="https://youtu.be/..." style="width:100%;margin-bottom:10px">';
		echo '<p style="margin:0 0 3px;font-size:11px;font-weight:600;color:#444">Podcast episode URL</p>';
		echo '<input type="url" name="ssd_pod" value="' . esc_attr( $pod ) . '" placeholder="https://open.spotify.com/episode/..." style="width:100%">';
		echo '<p style="color:#888;font-size:10px;margin:6px 0 0">Embeds above post content when filled in.</p>';
	}

	public function save_meta( $post_id ) {
		if ( ! isset( $_POST['ssd_media_nonce'] ) || ! wp_verify_nonce( $_POST['ssd_media_nonce'], 'ssd_save_media' ) ) return;
		if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) return;
		if ( ! current_user_can( 'edit_post', $post_id ) ) return;
		update_post_meta( $post_id, '_ssd_yt',  isset( $_POST['ssd_yt'] )  ? esc_url_raw( $_POST['ssd_yt'] )  : '' );
		update_post_meta( $post_id, '_ssd_pod', isset( $_POST['ssd_pod'] ) ? esc_url_raw( $_POST['ssd_pod'] ) : '' );
	}

	// ── YouTube / Podcast embed in content ────────────────────────────────────
	public function media_embeds( $content ) {
		if ( ! is_single() ) return $content;
		global $post;

		$yt  = get_post_meta( $post->ID, '_ssd_yt',  true );
		$pod = get_post_meta( $post->ID, '_ssd_pod', true );
		$pre = '';

		if ( $yt ) {
			$vid = null;
			if ( preg_match( '/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([A-Za-z0-9_\-]{11})/i', $yt, $m ) ) {
				$vid = $m[1];
			}
			if ( $vid ) {
				$pre .= '<div class="ssd-yt-embed"><div class="ssd-yt-wrap"><iframe src="https://www.youtube-nocookie.com/embed/' . esc_attr( $vid ) . '" allow="autoplay;encrypted-media;picture-in-picture" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="' . esc_attr( get_the_title( $post->ID ) ) . '"></iframe></div></div>';
			}
		}

		if ( $pod ) {
			$is_audio = preg_match( '/\.(mp3|ogg|wav|m4a|aac)(\?|$)/i', $pod );
			if ( $is_audio ) {
				$pre .= '<div class="ssd-audio"><p>&#127897; ' . esc_html( get_the_title( $post->ID ) ) . ' — Audio</p><audio controls><source src="' . esc_url( $pod ) . '" type="audio/mpeg"><a href="' . esc_url( $pod ) . '">Download episode</a></audio></div>';
			} else {
				$pre .= '<div class="ssd-pod">&#127897; <strong>Podcast:</strong> <a href="' . esc_url( $pod ) . '" target="_blank" rel="noopener noreferrer">Listen to this episode &rarr;</a></div>';
			}
		}

		return $pre . $content;
	}

	// ── Related Posts — styled card grid ──────────────────────────────────────
	public function related_posts( $content ) {
		if ( ! is_singular( 'post' ) || ! in_the_loop() ) return $content;
		global $post;

		$cats = wp_get_post_categories( $post->ID );
		$tags = wp_get_post_tags( $post->ID );
		if ( empty( $cats ) && empty( $tags ) ) return $content;

		$args = [
			'post_type'           => 'post',
			'post_status'         => 'publish',
			'posts_per_page'      => 4,
			'post__not_in'        => [ $post->ID ],
			'orderby'             => 'rand',
			'ignore_sticky_posts' => 1,
		];

		// Tag-based first (more specific)
		if ( ! empty( $tags ) ) {
			$args['tag__in'] = array_slice( wp_list_pluck( $tags, 'term_id' ), 0, 3 );
		}
		if ( ! empty( $cats ) ) {
			$args['category__in'] = $cats;
		}

		$related = get_posts( $args );

		// Fallback: category only
		if ( empty( $related ) && ! empty( $tags ) && ! empty( $cats ) ) {
			unset( $args['tag__in'] );
			$related = get_posts( $args );
		}

		if ( count( $related ) < 2 ) return $content;

		$html  = '<aside class="ssd-related-grid">';
		$html .= '<h3>You Might Also Like</h3>';
		$html .= '<div class="ssd-related-cards">';

		foreach ( $related as $r ) {
			$r_cats = get_the_category( $r->ID );
			$r_cat  = ! empty( $r_cats ) ? $r_cats[0]->name : '';
			$html  .= '<div class="ssd-related-card">';
			if ( $r_cat ) {
				$html .= '<span class="ssd-cat">' . esc_html( $r_cat ) . '</span>';
			}
			$html .= '<a href="' . esc_url( get_permalink( $r ) ) . '">' . esc_html( get_the_title( $r ) ) . '</a>';
			$html .= '<time datetime="' . esc_attr( get_the_date( 'c', $r ) ) . '">' . get_the_date( 'M j, Y', $r ) . '</time>';
			$html .= '</div>';
		}

		$html .= '</div></aside>';

		return $content . $html;
	}

	// ── Shortcodes ─────────────────────────────────────────────────────────────

	// [sourov_youtube video_id="XXXXXXXXXXX" title="Optional title"]
	public function sc_youtube( $atts ) {
		$atts = shortcode_atts( [ 'video_id' => '', 'title' => 'YouTube Video' ], $atts );
		if ( empty( $atts['video_id'] ) ) return '';
		return '<div class="ssd-yt-embed"><div class="ssd-yt-wrap"><iframe src="https://www.youtube-nocookie.com/embed/' . esc_attr( sanitize_text_field( $atts['video_id'] ) ) . '?rel=0" title="' . esc_attr( $atts['title'] ) . '" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade" style="border:0"></iframe></div></div>';
	}

	// [sourov_podcast src="URL" title="Episode Title"]
	public function sc_podcast( $atts ) {
		$atts = shortcode_atts( [ 'src' => '', 'title' => 'Listen to this episode' ], $atts );
		if ( empty( $atts['src'] ) ) return '';
		return '<div class="ssd-audio"><p>&#127897; ' . esc_html( $atts['title'] ) . '</p><audio controls><source src="' . esc_url( $atts['src'] ) . '" type="audio/mpeg"><a href="' . esc_url( $atts['src'] ) . '">Download</a></audio></div>';
	}

	// ── Sidebar Widget ─────────────────────────────────────────────────────────
	public function register_widget() {
		register_widget( 'SSD_YouTube_Widget' );
	}
}

// ── YouTube Channel Sidebar Widget ────────────────────────────────────────────
class SSD_YouTube_Widget extends WP_Widget {

	public function __construct() {
		parent::__construct( 'ssd_youtube_channel', 'Sourov — YouTube Channel', [
			'description' => 'YouTube channel subscribe button for the sidebar.',
		] );
	}

	public function widget( $args, $instance ) {
		echo $args['before_widget'];
		$title = ! empty( $instance['title'] ) ? $instance['title'] : 'Watch on YouTube';
		echo $args['before_title'] . esc_html( $title ) . $args['after_title'];
		$yt_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>';
		echo '<div class="ssd-yt-widget"><a href="' . esc_url( SSD_YT_CHANNEL_URL ) . '" target="_blank" rel="noopener noreferrer" aria-label="Subscribe on YouTube">' . $yt_icon . ' Subscribe</a><p>' . esc_html( SSD_YT_CHANNEL_NAME ) . '</p></div>';
		echo $args['after_widget'];
	}

	public function form( $instance ) {
		$title = ! empty( $instance['title'] ) ? $instance['title'] : 'Watch on YouTube';
		echo '<p><label for="' . $this->get_field_id('title') . '">Title: <input class="widefat" id="' . $this->get_field_id('title') . '" name="' . $this->get_field_name('title') . '" type="text" value="' . esc_attr($title) . '"></label></p>';
	}

	public function update( $new, $old ) {
		return [ 'title' => sanitize_text_field( $new['title'] ) ];
	}
}

new Sourov_Site_Enhancer();
