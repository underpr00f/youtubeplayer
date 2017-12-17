var gulp = require('gulp'),
  sass = require('gulp-sass');
  //browserSync = require('browser-sync').create();
    //reload = browserSync.reload;
/*
var autoprefixer = require('gulp-autoprefixer');
 
gulp.task('pref', function () {
    return gulp.src('static/styles/compiled/sass.css')
        .pipe(autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
        }))
        .pipe(gulp.dest('static/styles/compiled'));
});
*/
gulp.task('sass', function() {
  return gulp.src('static/styles/*.scss') // Gets all files ending with .scss in app/scss and children dirs
    .pipe(sass())
    .pipe(gulp.dest('static/styles/compiled'))
    //.pipe(reload({stream: true}))
});
/*
gulp.task('browserSync', function() {
  browserSync.init({
    notify: false,
    port: 8000,
    proxy: 'localhost:8000'
  })
});
*/
//gulp.task('watch', ['sass', 'browserSync'], function() {
gulp.task('watch', ['sass',], function() {
  gulp.watch('static/styles/*.scss', ['sass']);
  //gulp.watch('static/js/*.js', reload({stream: true}));
  //gulp.watch('templates/**/*.html', reload({stream: true}));
});

gulp.task('default', ['watch']);
//var django = require('gulp-django-utils');
//var concat = require('gulp-concat');

// Initialize application list for processing.
//var apps = ['player','registration','socialprofile','chat','friendship'];

// Initialize project with apps in current directory.
//var project = new django.Project(apps);

// Create a task which depends on the same tasks in apps.
//project.task('js', function() {
  // Take all `.js` files from `django-project/static/main/js`,
  // concatenate it and put to `django-project/static/build`.
  //project.src('static/js/*.js')
    //.pipe(concat('main.js'))
    //.pipe(project.dest('static/build'));
//});

