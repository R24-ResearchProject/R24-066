const Review = require('../models/Review');

class ReviewService {
  async getAllReviews() {
    return await Review.find();
  }

  async createReview(reviewData) {
    return await Review.create(reviewData);
  }

  async getReviewById(id) {
    return await Review.findById(id);
  }

  async deleteReviewById(id) {
    return await Review.findByIdAndDelete(id);
  }

  async updateReviewById(id, updateData) {
    return await Review.findByIdAndUpdate(id, updateData, { new: true });
  }

  async getReviewsByUsername(username) {
    return await Review.find({ user: username });
  }

  async getReviewsByActivity(activity) {
    return await Review.find({ activity: activity });
  }

  async getReviewsBySubject(subject) {
    return await Review.find({ subject: subject });
  }
  // async getReviewsBySubjectUser(subject, username) {
  //   return await Review.find({ subject: subject,  user: username });
  // }

  async getReviewsBySubjectUser(subject, username) {
    return await Review.aggregate([
      {
        $match: {
          $and: [
            { subject: subject },
            { user: username }
          ]
        }
      },
      {
        $sort: { reviewDate: -1 } // Sort by reviewDate in descending order
      },
      {
        $group: {
          _id: { $dateToString: { format: "%Y-%m-%d", date: "$reviewDate" } }, // Group by date
          latestReview: { $first: "$$ROOT" } // Take the first document (latest) in each group
        }
      },
      {
        $replaceRoot: { newRoot: "$latestReview" } // Replace the root with the latestReview document
      }
    ]);
  }
  async getReviewsSearch(subject, activity, username) {
    return await Review.find({
      $and: [
        { subject: subject },
        { activity: activity },
        { user: username }
      ]
    }).sort({ reviewDate: 1 }); 
  }

  async getReviewsSearch(subject, activity, username) {
    return await Review.aggregate([
      {
        $match: {
          $and: [
            { subject: subject },
            { activity: activity },
            { user: username }
          ]
        }
      },
      {
        $sort: { reviewDate: -1 } // Sort by reviewDate in descending order
      },
      {
        $group: {
          _id: { $dateToString: { format: "%Y-%m-%d", date: "$reviewDate" } }, // Group by date
          latestReview: { $first: "$$ROOT" } // Take the first document (latest) in each group
        }
      },
      {
        $replaceRoot: { newRoot: "$latestReview" } // Replace the root with the latestReview document
      }
    ]);
  }
}

module.exports = ReviewService;
