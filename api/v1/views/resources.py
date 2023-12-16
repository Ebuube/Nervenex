#!/usr/bin/python3
"""
Objects that handle all default RestFul API actions for Resources
"""
from models import storage
from models.resource import Resource
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/resources', methods=['GET'], strict_slashes=False)
@swag_from('documentation/resource/all_resources.yml')
def get_resources():
    """Get all Resources"""
    all_resources = storage.all(Resource).values()
    list_resources = []
    for resource in all_resources:
        list_resources.append(resource.to_dict())

    return jsonify(list_resources)


@app_views.route('/resources/<type>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/resource/get_resources_by_type.yml')
def get_resources_by_type(type):
    """Get resources by type"""
    resources_by_type = storage.all(Resource).filter(
        Resource.type == type).values()
    list_resources = []
    for resource in resources_by_type:
        list_resources.append(resource.to_dict())

    return jsonify(list_resources)


@app_views.route('/resources/<resource_id>',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/resource/get_resource.yml', methods=['GET'])
def get_resource(resource_id):
    """Get a specific resource"""
    resource = storage.get(Resource, resource_id)
    if not resource:
        abort(404, description="Resource not found")

    return jsonify(resource.to_dict())


@app_views.route('/resources', methods=['POST'], strict_slashes=False)
@swag_from('documentation/resource/post_resource.yml', methods=['POST'])
def create_resource():
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if not data.get('title') or not data.get('author_id') or not data.get(
            'type') or not data.get('link') or not data.get('description'):
        abort(400, description="Missing required fields")

    author = storage.get(User, data['author_id'])
    if not author:
        abort(400, description="Invalid author_id")

    instance = Resource(**data)
    storage.save(instance)
    resource = instance.to_dict()

    return make_response(jsonify(resource), 201)


@app_views.route('/resources/<resource_id>',
                 methods=['PUT'], strict_slashes=False)
@swag_from('documentation/resource/put_resource.yml', methods=['PUT'])
def update_resource(resource_id):
    """Update a Resource"""
    resource = storage.get(Resource, resource_id)
    if not resource:
        abort(404, decription="Resource not found")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at', 'author_id']

    for key, value in data.items():
        if key not in ignore:
            setattr(resource, key, value)
    storage.save()
    resource = resource.to_dict()

    return make_response(jsonify(resource), 200)


@app_views.route('/resources/<resource_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/resource/delete_resource.yml', methods=['DELETE'])
def delete_resource(resource_id):
    """Delete a resource"""
    resource = storage.get(Resource, resource_id)
    if not resource:
        abort(404, description="Resource is not available")

    storage.delete(resource)
    storage.save()

    return make_response(
        jsonify({'description': 'Resource deleted successfully'}), 200)
