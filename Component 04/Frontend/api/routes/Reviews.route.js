const express = require('express');
const { body } = require('express-validator');
const ReviewController = require('../controllers/Reviews.controller');

const router = express.Router();
const reviewController = new ReviewController();

router.post('/', [
  // Add validation middleware if required
], reviewController.createReview.bind(reviewController));

router.get('/', reviewController.getAllReviews.bind(reviewController));

router.get('/:id', reviewController.getReviewById.bind(reviewController));

router.delete('/:id', reviewController.deleteReviewById.bind(reviewController));

router.put('/:id', [
  // Add validation middleware if required
], reviewController.updateReviewById.bind(reviewController));

router.get('/user/:username', reviewController.getReviewsByUsername.bind(reviewController));

router.get('/activity/:activity', reviewController.getReviewsByActivity.bind(reviewController));

router.get('/subject/:subject', reviewController.getReviewsBySubject.bind(reviewController));

router.get('/subject/:subject/byUser/:username', reviewController.getReviewsBySubjectUser.bind(reviewController));

router.get('/search/:subject/byActivity/:activity/byUser/:username', reviewController.getReviewsSearch.bind(reviewController));

module.exports = router;
