from grpc_tools import protoc


match_text = '\nimport sgd_pb2 as sgd__pb2\n'
replace_text = '''
try:
    # for grpc server
    import proto.sgd_pb2 as sgd__pb2
except ModuleNotFoundError:
    # for django
    import sgd_grpc.proto.sgd_pb2 as sgd__pb2
'''


protoc.main((
    '',
    '-I./proto',
    '--python_out=./proto',
    '--grpc_python_out=./proto',
    'proto/sgd.proto'
))

# Add import declarations for grpc and django applications
replace_content = ''

with open('proto/sgd_pb2_grpc.py', 'r+') as f:
    content_file = f.read()
    replace_content = content_file.replace(match_text, replace_text)

with open('proto/sgd_pb2_grpc.py', 'w') as f:
    f.write(replace_content)
