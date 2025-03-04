import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

# View Imports 
from views import list_posts, retrieve_post
from views import list_tags 
from views import list_categories
from views import create_user, login_user

class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for Rare"""

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "posts":
            if url["pk"] != 0:
                response_body = retrieve_post(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_posts()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "tags":
            response_body = list_tags()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        elif url["requested_resource"] == "categories":
            response_body = list_categories()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
            
        else:
            return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        


    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        data = json.loads(request_body)

        url = self.parse_url(self.path)

        if url["requested_resource"] == "users":
            response_body = create_user(data)
            if response_body:                                   
                return self.response(json.dumps(response_body), status.HTTP_201_SUCCESS_CREATED.value)
            return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        
        else:
            return self.response("Resource not found", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)

    def do_DELETE(self):
        """Handle DELETE Requests from the client"""
        pass

    def do_PUT(self):
        """Handle PUT requests from the client"""
        pass

# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES BUT IMPORTANT FOR SETTING THE RIGHT PORT TO LISTEN TO
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()
    print("SERVER IS RUNNING... MAYBE???")