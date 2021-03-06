"""
Details the various flask endpoints for processing and retrieving
command details as well as a swagger spec endpoint
"""

from multiprocessing import Process, Queue
import sys
from flask import Flask, request, jsonify
from flask_swagger import swagger

from db import session, engine
from base import Base, Command
from command_parser import get_valid_commands, process_command_output

app = Flask(__name__)


@app.route('/commands', methods=['GET'])
def get_command_output():
    """
    Returns as json the command details that have been processed
    to date.
    ---
    tags: [commands]
    responses:
      200:
        description: Commands returned OK
      400:
        description: Commands not found
    """
    commands = session.query(Command).all()
    # TODO: format the query result
    # return jsonify(commands)
    return jsonify([
        {
        'command_id': command.id,
        'command_string': command.command_string,
        'length': command.length,
        'duration': command.duration,
        'output': str(command.output)
        }
        for command in commands
        ])



@app.route('/commands', methods=['POST'])
def process_commands():
    """
    Processes commands from a command list
    ---
    tags: [commands]
    parameters:
      - name: filename
        in: formData
        description: filename of the commands text file to parse
                     which exists on the server
        required: true
        type: string
    responses:
      200:
        description: Processing OK
    """
    # filename = request.args.get('filename').filename

     # get the filename
    file = request.files.get('filename')
    filename = file.filename

    queue = Queue()
    get_valid_commands(queue, filename)
    process_command_output(queue)


    # processes = [Process(target=process_command_output, args=(queue,))
    #              for num in range(2)]
    # for process in processes:
    #     process.start()
    # for process in processes:
    #     process.join()
    # return 'Successfully processed commands.'
    return 'Successfully processed commands. \n'



@app.route('/database', methods=['POST'])
def make_db():
    """
    Creates database schema
    ---
    tags: [db]
    responses:
      200:
        description: DB Creation OK
    """
    Base.metadata.create_all(engine)
    # return 'Database creation successful.'
    return 'Database creation successful. \n'


@app.route('/database', methods=['DELETE'])
def drop_db():
    """
    Drops all db tables
    ---
    tags: [db]
    responses:
      200:
        description: DB table drop OK
    """
    Base.metadata.drop_all(engine)
    # return 'Database deletion successful.'
    return 'Database deletion successful. \n'



@app.route('/spec', methods=['GET'])
def swagger_spec():
    """
    Display the swagger formatted JSON API specification.
    ---
    tags: [docs]
    responses:
      200:
        description: OK status
    """
    spec = swagger(app)
    spec['info']['title'] = "Intel AI DLS coding challenge API"
    spec['info']['description'] = ("Intel AI deep learning systems coding " +
                                   "challenge for interns and full-time hires")
    spec['info']['license'] = {
        "name": "Intel Proprietary License",
        "url": "https://ai.intel.com",
    }
    spec['info']['contact'] = {
        "name": "Intel DLS Team",
        "url": "https://ai.intel.com",
        "email": "scott.leishman@intel.com",
    }
    spec['schemes'] = ['http']
    spec['tags'] = [
        {"name": "db", "description": "database actions (create, delete)"},
        {"name": "commands", "description": "process and retrieve commands"}
    ]
    return jsonify(spec)


if __name__ == '__main__':
    """
    Starts up the flask server
    """
    port = 8080
    use_reloader = True

    # provides some configurable options
    for arg in sys.argv[1:]:
        if '--port' in arg:
            port = int(arg.split('=')[1])
        elif '--use_reloader' in arg:
            use_reloader = arg.split('=')[1] == 'true'

    # app.run(port=port, debug=True, use_reloader=use_reloader)

    # add host address here for being able to use docker
    app.run(host='0.0.0.0',port=port, debug=True, use_reloader=use_reloader)
