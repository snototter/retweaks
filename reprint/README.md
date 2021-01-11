TODO

Subfolder `ppd` contains the PostScript Printer Description (`.ppd` file) to install the printer on your host (Add printer > ipp://<IP>:<PORT> > provide PPD)  
https://www.cups.org/doc/postscript-driver.html

ppd generated from the driver information file `.drv` via [`ppdc`](https://www.cups.org/doc/ppd-compiler.html)





TODOs
* [x] get (somewhat) familiar with PPD
* [x] try python ipp server (simply dumping the pdf chunks worked nicely)
* [ ] cpp/qt ipp server
  * [ ] implement basic server
  * [ ] implement stateless ipp printing
  * [ ] implement status responses
* Potential networking frameworks:
  * https://github.com/qt-labs/qthttpserver/blob/master/examples/httpserver/simple/main.cpp#L59 (qt cross compilation is what rm does and I can focus on IPP and don't have to worry about tcp & http)
  * https://github.com/sprinfall/webcc  (simple(r) cpp asio framework)
  * http://think-async.com/Asio/Download.html  (quite complex at the first glance)
  * https://github.com/chronoxor/CppServer (dependencies will likely cause me a headache during cross compilation)
  * apt install `moreutils` to query error numbers via `errno` (if working directly with [c sockets](https://ncona.com/2019/04/building-a-simple-server-with-cpp/))
