//#include <httpserver.hpp>

//using namespace httpserver;

//class hello_world_resource : public http_resource
//{
//public:
//  const std::shared_ptr<http_response> render(const http_request&)
//  {
//    return std::shared_ptr<http_response>(new string_response("Hello, World!"));
//  }
//};

//int main(int argc, char** argv)
//{
//  webserver ws = create_webserver(8080);

//  hello_world_resource hwr;
//  ws.register_resource("/hello", &hwr);
//  ws.start(true);

//  return 0;
//}


#include <httpserver.hpp>

using namespace httpserver;

class user_pass_resource : public httpserver::http_resource {
public:
    const std::shared_ptr<http_response> render_GET(const http_request& req) {
        if (req.get_user() != "myuser" || req.get_pass() != "mypass") {
            return std::shared_ptr<basic_auth_fail_response>(new basic_auth_fail_response("FAIL", "test@example.com"));
        }
        return std::shared_ptr<string_response>(new string_response(req.get_user() + " " + req.get_pass(), 200, "text/plain"));
    }
};

int main(int argc, char** argv) {
    webserver ws = create_webserver(8080);

    user_pass_resource hwr;
    ws.register_resource("/hello", &hwr);
    ws.start(true);

    return 0;
}
