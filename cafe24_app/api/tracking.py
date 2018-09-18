from . import api


@api.route('/tracking/<int:id>')
def get_orders(id):
