namespace cpp tis
namespace py tis
namespace php tis

struct SendSMSRequest {
    1: required string mobile;//发送手机号，可以多个，逗号分隔
    2: required string content;//发送内容
    3: required i32 send_time=0;
}

service SmsService {
    i32 send_sms(1: SendSMSRequest request),
    bool heart_beat(),
}

