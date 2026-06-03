<?php
/**
 * Plugin Name:  Sourov Health Monitor
 * Plugin URI:   https://github.com/sourovdeb/wordpress-control
 * Description:  Adds GET /wp-json/sourov/v1/health for automated health checks.
 *               Authentication via X-Sourov-Key header.
 *               Set SOUROV_API_KEY in wp-config.php or store in options.
 * Version:      1.0.0
 * Author:       Sourov Deb
 * License:      MIT
 *
 * Installation:
 *   1. Upload this file to /wp-content/plugins/sourov-health-monitor/
 *   2. Activate in Plugins > Installed Plugins
 *   3. Add to wp-config.php:
 *      define( 'SOUROV_API_KEY', 'your-key-here' );
 *   4. Test: GET https://yourdomain.com/wp-json/sourov/v1/health
 *      Header: X-Sourov-Key: your-key-here
 */

defined( 'ABSPATH' ) || exit;

add_action( 'rest_api_init', function () {
    register_rest_route( 'sourov/v1', '/health', [
        'methods'             => 'GET',
        'callback'            => 'sourov_health_handler',
        'permission_callback' => 'sourov_check_api_key',
    ] );
} );

/**
 * Validate the X-Sourov-Key header using a constant-time comparison.
 */
function sourov_check_api_key( WP_REST_Request $request ): bool {
    $provided = (string) $request->get_header( 'X-Sourov-Key' );
    $stored   = defined( 'SOUROV_API_KEY' )
        ? SOUROV_API_KEY
        : (string) get_option( 'sourov_api_key', '' );
    return $stored !== '' && hash_equals( $stored, $provided );
}

/**
 * Return a health payload with site metadata.
 */
function sourov_health_handler(): WP_REST_Response {
    global $wpdb;

    $db_ok = false;
    try {
        $wpdb->get_var( 'SELECT 1' );
        $db_ok = ( $wpdb->last_error === '' );
    } catch ( Exception $e ) {
        // db unavailable
    }

    $post_counts = wp_count_posts();
    $theme       = wp_get_theme();

    $data = [
        'status'          => $db_ok ? 'healthy' : 'degraded',
        'timestamp'       => current_time( 'c' ),
        'wp_version'      => get_bloginfo( 'version' ),
        'php_version'     => PHP_VERSION,
        'site_url'        => get_site_url(),
        'home_url'        => get_home_url(),
        'database_ok'     => $db_ok,
        'active_plugins'  => count( (array) get_option( 'active_plugins', [] ) ),
        'theme'           => $theme->get( 'Name' ) . ' ' . $theme->get( 'Version' ),
        'posts_published' => (int) ( $post_counts->publish ?? 0 ),
        'posts_draft'     => (int) ( $post_counts->draft   ?? 0 ),
        'memory_used_mb'  => round( memory_get_usage( true ) / 1048576, 1 ),
        'memory_limit'    => ini_get( 'memory_limit' ),
        'upload_max_mb'   => ini_get( 'upload_max_filesize' ),
        'debug_mode'      => defined( 'WP_DEBUG' ) && WP_DEBUG,
        'cron_disabled'   => defined( 'DISABLE_WP_CRON' ) && DISABLE_WP_CRON,
    ];

    $code = $db_ok ? 200 : 503;
    return new WP_REST_Response( $data, $code );
}
