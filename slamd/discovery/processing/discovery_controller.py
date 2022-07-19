from flask import Blueprint, render_template

from slamd.discovery.processing.discovery_service import DiscoveryService

discovery = Blueprint('discovery', __name__,
                      template_folder='../templates',
                      static_folder='../static',
                      static_url_path='static',
                      url_prefix='/materials/discovery')

discovery_service = DiscoveryService()


@discovery.route('', methods=['GET'])
def discovery_page():
    return render_template('discovery.html')
