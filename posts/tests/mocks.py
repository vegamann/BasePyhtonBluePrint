from httmock import HTTMock, all_requests, response

@all_requests
def mock_success_auth(url, request):
  return response(200, { 'id': 1 }, {}, None, 5, request)

@all_requests
def mock_failed_auth(url, request):
  return { 'status_code': 401 }