const ReviewService = require('../services/Reviews.service');

class ReviewController {
  constructor() {
    this.reviewService = new ReviewService();
  }

  async getAllReviews(req, res) {
    try {
      const reviews = await this.reviewService.getAllReviews();
      res.json(reviews);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async createReview(req, res) {
    try {
      const newReview = await this.reviewService.createReview(req.body);
      res.status(201).json(newReview);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }

  async getReviewById(req, res) {
    try {
      const review = await this.reviewService.getReviewById(req.params.id);
      res.json(review);
    } catch (error) {
      res.status(404).json({ error: 'Review not found' });
    }
  }

  async deleteReviewById(req, res) {
    try {
      await this.reviewService.deleteReviewById(req.params.id);
      res.sendStatus(204);
    } catch (error) {
      res.status(404).json({ error: 'Review not found' });
    }
  }

  async updateReviewById(req, res) {
    try {
      const updatedReview = await this.reviewService.updateReviewById(req.params.id, req.body);
      res.json(updatedReview);
    } catch (error) {
      res.status(404).json({ error: 'Review not found' });
    }
  }

  async getReviewsByUsername(req, res) {
    try {
      const reviews = await this.reviewService.getReviewsByUsername(req.params.username);
      res.json(reviews);
    } catch (error) {
      res.status(404).json({ error: 'Reviews not found for the user' });
    }
  }

  async getReviewsByActivity(req, res) {
    try {
      const reviews = await this.reviewService.getReviewsByActivity(req.params.activity);
      res.json(reviews);
    } catch (error) {
      res.status(404).json({ error: 'Reviews not found for the activity' });
    }
  }

  async getReviewsBySubject(req, res) {
    try {
      const reviews = await this.reviewService.getReviewsBySubject(req.params.subject);
      res.json(reviews);
    } catch (error) {
      res.status(404).json({ error: 'Reviews not found for the subject' });
    }
  }
  
  async getReviewsBySubjectUser(req, res) {
    try {
      const reviews = await this.reviewService.getReviewsBySubjectUser(req.params.subject, req.params.username);
      res.json(reviews);
    } catch (error) {
      res.status(404).json({ error: 'Reviews not found for the subject' });
    }
  }

  async getReviewsSearch(req, res) {
    try {
      const reviews = await this.reviewService.getReviewsSerach(req.params.subject, req.params.activity, req.params.username);
      res.json(reviews);
    } catch (error) {
      res.status(404).json({ error: 'Reviews not found for the subject' });
    }
  }
}

module.exports = ReviewController;
