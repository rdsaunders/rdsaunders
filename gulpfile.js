// Load the module.
var gulp = require( 'gulp' );
var svgSprite = require( 'gulp-svg-sprite' );

// Set our desired configuration values.
svgConfig = {
    mode: {
        symbol: true
    },
    svg: {
        xmlDeclaration: false,
        doctypeDeclaration: false,
        // By default the module wants to namespace
        // all our IDs and classes. We're grownups
        // so we want to preserve our settings.
        namespaceIDs: false,
        namespaceClassnames: false
    }
};

// Define our task.
gulp.task('svg', function(done) {
    // Set the source folder.
    gulp.src( 'images/svg/**/*.svg' )
        // Include our options.
        .pipe( svgSprite( svgConfig ) )
        // Set the destination folder.
        .pipe( gulp.dest( '_includes' ) );
    done();
});
