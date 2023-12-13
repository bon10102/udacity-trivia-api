import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.app_context().push()
    if test_config is None:
        setup_db(app)

    """
    DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"*": {"origins": "*"}})

    """
    DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,DELETE"
        )
        return response

    """
    DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=['GET'])
    def get_all_categories():
        categories = Category.query.order_by('type').all()
        formatted_categories = {category.id: category.type for category in categories}
        if (len(categories) == 0):
            abort(404)
        db.session.close()
        return jsonify({
            'success': True,
            'categories': formatted_categories
        }), 200

    """
    DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=['GET'])
    def get_all_questions():
        questions = Question.query.order_by('id').all()
        categories = Category.query.order_by('id').all()
        formatted_categories = {category.id: category.type for category in categories}
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(questions),
            "categories": formatted_categories,
            "current_category": None,
        }), 200

    """
    DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        error = False
        try:
            question = db.session.get(Question, question_id)
            if question is None:
                error = True
            question.delete()
            updated_questions = Question.query.order_by('id').all()
            current_questions = paginate_questions(request, updated_questions)
        except:
            abort(422)
        finally:
            if error:
                abort(404)
            else:
                return jsonify({
                    "success": True,
                    "deleted": question_id,
                }), 200

    """
    DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        if body.get("question", None) is None:
            abort(400)
        try:
            question = Question(
                question = body.get("question", None),
                answer = body.get("answer", None),
                difficulty = body.get("difficulty", None),
                category = body.get("category", None),
            )
            question.insert()

            updated_questions = Question.query.order_by('id').all()
            current_questions = paginate_questions(request, updated_questions)
            return jsonify({
                "success": True,
                "created": question.id,
                "questions": current_questions,
                "total_questions": len(updated_questions)
            }), 200
        except:
            abort(422)

    """
    DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = "%" + body["searchTerm"] + "%"
        questions = Question.query.filter(Question.question.ilike(search_term)).order_by('id').all()
        if len(questions) == 0:
            abort(404)
        try:
            current_questions = paginate_questions(request, questions)
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
            }), 200
        except:
            abort(422)

    """
    DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_category_questions(category_id):
        category = db.session.get(Category, category_id)
        if category is None:
            abort(404)
        try:
            category_questions = Question.query.filter_by(category=category_id).order_by('id').all()
            current_questions = paginate_questions(request, category_questions)
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(category_questions),
                "current_category": category_id,
            }), 200
        except:
            abort(422)

    """
    DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=['POST'])
    def play_quiz():
        body = request.get_json()
        if "previous_questions" and "quiz_category" not in body:
            abort(400)
        try:
            previous_questions = body["previous_questions"]
            category = body["quiz_category"]
            remaining_questions = []
            #all categories
            if (category["id"] == 0):
                remaining_questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
            #specific category
            else:
                remaining_questions = Question.query.filter_by(category=category["id"]).filter(Question.id.notin_((previous_questions))).all()
            
            if len(remaining_questions) >= 1:
                question = remaining_questions[random.randrange(0, len(remaining_questions))].format()
                return jsonify({
                    "success": True,
                    "question": question,
                }), 200
            else:
                return jsonify({
                    "success": True,
                    "question": None,
                }), 200
        except:
            abort(422)

    """
    DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )
    
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "internal server error"})
        )

    return app

