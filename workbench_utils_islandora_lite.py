import os
import sys
import json
import csv
import openpyxl
import time
import string
import re
import copy
import logging
import datetime
import requests
import subprocess
import hashlib
import mimetypes
import collections
import urllib.parse
from pathlib import Path
from ruamel.yaml import YAML, YAMLError
import shutil

sys.path.insert(1, '../../islandora_workbench')
from workbench_utils import *
from workbench_utils_islandora_lite import *


yaml = YAML()

def validate_file_name(filename):
    """Creates a media in Drupal.

           Parameters
           ----------
            filename : string
                The value of the CSV 'file' field for the current node.
            Returns
            -------
            int|False
                 Not a valid filename
    """
    try:
        # We need to test that the filename is valid Latin-1 since Requests requires that.
        filename.encode('latin-1')
    except UnicodeError:
        logging.error("Filename " + filename + " is not valid Latin-1.")
        return False

    try:
        # We also need to test that the filename is valid UTF-8 since Drupal requires that.
        filename.encode('utf-8')
    except UnicodeError:
        logging.error("Filename " + filename + " is not valid UTF-8.")
        return False

def create_media_islandora_lite(config, filename, node_id, node_csv_row):
    """Creates a media in Drupal.

           Parameters
           ----------
            config : dictfilename
                The configuration object defined by set_config_defaults().
            filename : string
                The value of the CSV 'file' field for the current node.
            node_id: string
                The ID of the node to attach the media to. This is False if file creation failed.
            node_csv_row: OrderedDict
                E.g., OrderedDict([('file', 'IMG_5083.JPG'), ('id', '05'), ('title', 'Alcatraz Island').
            Returns
            -------
            int|False
                 The HTTP status code from the attempt to create the media, False if
                 it doesn't have sufficient information to create the media, or None
                 if config['nodes_only'] is True.
    """
    if config['nodes_only'] is True:
        return

    validate_file_name(filename)

    file_result = create_file(config, filename, "file", node_csv_row, node_id)

    if isinstance(file_result, int):

        if filename.startswith('http'):
            parts = urllib.parse.urlparse(filename)
            filename = parts.path
        media_type = set_media_type(config, filename, "file", node_csv_row)
        media_field = config['media_fields'][media_type]


        media_use_tid_value = node_csv_row['media_use_tid']
        media_use_tids = []
        media_use_terms = str(media_use_tid_value).split(config['subdelimiter'])
        for media_use_term in media_use_terms:
            if value_is_numeric(media_use_term):
                media_use_tids.append(media_use_term)
            if not value_is_numeric(media_use_term) and media_use_term.strip().startswith('http'):
                media_use_tids.append(get_term_id_from_uri(config, media_use_term))
            if not value_is_numeric(media_use_term) and not media_use_term.strip().startswith('http'):
                media_use_tids.append(find_term_in_vocab(config, 'islandora_media_use', media_use_term.strip()))

        # Patch FITS info
        if "fits" in node_csv_row and len(node_csv_row["fits"]) > 0:
            file_endpoint = config['host'] + '/file/' + str(file_result) + '?_format=json'
            file_headers = {'Content-Type': 'application/json'}
            file_json = {
                "type": [{
                    "target_id": media_type
                }],
                "field_fits": [{
                    "value": node_csv_row['fits']
                }]
            }
            try:
                file_response = issue_request(config, 'PATCH', file_endpoint, file_headers, file_json)
                if file_response.status_code not in [200]:
                    logging.error("Unable to update FITS info")
            except:
                logging.error("Unable to update FITS info")

        # Put custom thumbnail if it exists
        file_result_thumbnail = False
        if "field_custom_thumbnail" in node_csv_row and len(node_csv_row["field_custom_thumbnail"]) > 0:
            node_csv_row_for_thumbnail = dict(node_csv_row)

            node_csv_row_for_thumbnail["file"] = node_csv_row["field_custom_thumbnail"]
            validate_file_name(node_csv_row["field_custom_thumbnail"])
            file_result_thumbnail = create_file(config, node_csv_row["field_custom_thumbnail"], node_csv_row_for_thumbnail)

        media_json = {
            "bundle": [{
                "target_id": media_type,
                "target_type": "media_type",
            }],
            "status": [{
                "value": True
            }],
            "name": [{
                "value": node_csv_row['title']
            }],
            "name": [{
                "value": node_csv_row['title']
            }],
            "field_media_use": [{
                "target_id": media_use_tids[0],
                "target_type": 'taxonomy_term'
            }],
            media_field: [{
                "target_id": file_result,
                "target_type": 'file'
            }]
        }

        if "field_base_url" in node_csv_row and len(node_csv_row["field_base_url"]) > 0:
            media_json["field_base_url"] = [{
                "uri": node_csv_row['field_base_url']
            }]

        file_result_multi = False
        if "ableplayer_caption" in node_csv_row and len(node_csv_row["ableplayer_caption"]) > 0:
            transcripts = str(node_csv_row["ableplayer_caption"]).split(config['subdelimiter'])
            file_result_multi = False

            for transcript in transcripts:
                transcript = transcript.strip()

                node_csv_row_copy = dict(node_csv_row)
                node_csv_row_copy["file"] = transcript
                validate_file_name(node_csv_row_copy["file"])
                file_result_multi = create_file(config, node_csv_row_copy["file"], "file", node_csv_row_copy, node_id)

                if isinstance(file_result_multi, int):
                    media_json["ableplayer_caption"] = [{
                        "target_id": file_result_multi,
                        "target_type": 'file'
                    }]

        # TODO: We'll need a more generalized way of determining which media fields are required.
        if media_field == 'field_media_image':
            if 'image_alt_text' in node_csv_row and len(node_csv_row['image_alt_text']) > 0:
                alt_text = clean_image_alt_text(node_csv_row['image_alt_text'])
                media_json[media_field][0]['alt'] = alt_text
            else:
                alt_text = clean_image_alt_text(node_csv_row['title'])
                media_json[media_field][0]['alt'] = alt_text

        media_endpoint_path = '/entity/media?_format=json'
        media_headers = {
            'Content-Type': 'application/json'
        }

        try:
            media_response = issue_request(config, 'POST', media_endpoint_path, media_headers, media_json)

            allowed_media_response_codes = [201, 204]
            if media_response.status_code in allowed_media_response_codes:

                if len(media_use_tids) > 1:
                    media_response_body = json.loads(media_response.text)
                    if 'mid' in media_response_body:
                        media_id = media_response_body['mid'][0]['value']
                        patch_media_use_terms(config, media_id, media_type, media_use_tids)
                    else:
                        logging.error("Could not PATCH additional media use terms to media created from '%s' because media ID is not available.", filename)


                print("media successfully created")
                media_json = json.loads(media_response.text)
                mid = media_json['mid'][0]['value']

                node = {
                    'type': [
                        {'target_id': "islandora_object"}
                    ]
                }

                node['field_islandora_object_media'] = [{
                    "target_id": mid,
                    "target_type": 'media'
                }]

                # If append_media is True
                if "append_media" in config and config["append_media"] == True:
                    node_media_list = get_node_media_from_nid(config, node_csv_row['node_id'])

                    if len(node_media_list) > 0:
                        current_media = {"target_id": mid, "target_type": 'media'}
                        node_media_list.append(current_media)
                        node['field_islandora_object_media'] = node_media_list

                node_endpoint = config['host'] + '/node/' + node_csv_row['node_id'] + '?_format=json'
                node_headers = {'Content-Type': 'application/json'}
                node_response = issue_request(config, 'PATCH', node_endpoint, node_headers, node)

                # Execute media-specific post-create scripts, if any are configured.
                if 'media_post_create' in config and len(config['media_post_create']) > 0:
                    for command in config['media_post_create']:
                        post_task_output, post_task_return_code = execute_entity_post_task_script(command, config['config_file_path'], media_response.status_code, media_response.text)
                        if post_task_return_code == 0:
                            logging.info("Post media create script " + command + " executed successfully.")
                        else:
                            logging.error("Post media create script " + command + " failed.")

                return node_response.status_code
            else:
                print("media creation failed")
                return False
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return False

    if file_result is False:
        return file_result

    if file_result is None:
        return file_result

def get_node_media_from_nid(config, node_id):
    """Get node field_islandora_object_media from Drupal.

    """
    node_url = config['host'] + '/node/' + node_id + '?_format=json'
    node_response = issue_request(config, 'GET', node_url)
    if node_response.status_code == 200:
        node_dict = json.loads(node_response.text)
        return node_dict['field_islandora_object_media']
    else:
        return False

