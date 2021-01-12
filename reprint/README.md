TODO

Since I wanted to learn how to cross-compile applications for the remarkable2 and liked the simplicity of the [go-based AppSocket printer](https://github.com/Evidlo/remarkable_printer) (leverage native printing capabilities, doesn't need rm cloud), I started working on this c++ IPP server/printing service.

Subfolder `ppd` contains the PostScript Printer Description (`.ppd` file) to install the printer on your host (Add printer > ipp://<IP>:<PORT> > provide PPD)  
https://www.cups.org/doc/postscript-driver.html

ppd generated from the driver information file `.drv` via [`ppdc`](https://www.cups.org/doc/ppd-compiler.html)





TODOs
* [x] get (somewhat) familiar with PPD
* [x] try python ipp server (simply dumping the pdf chunks worked nicely)
  * Maybe expose the PPD via HTTP GET (e.g. `<IP>:<PORT>/ppd`)?
  * Maybe provide a landing page for other HTTP GET requests?
    ```
    INFO:root:Listening on ('127.0.0.1', 9100)
    # http://<ip>:<port>
    DO GET path: [/]
    DO GET path: [/favicon.ico]
    # http://<ip>:<port>/ppd
    DO GET path: [/ppd]
    # Print via CUPS
    DO POST [/]
    DO POST [/]
    DO POST [/]
    DO POST [/]
    DO POST [/]
    INFO:root:Saving print job as '/tmp/ipp-server-print-job-7bb2e6ca-545c-11eb-a9a0-10bf48d816cc.pdf'
    DO POST [/]
    DO POST [/]
    DO POST [/]
    DO POST [/]
    DO POST [/]
    ```
* [ ] refresh my qt knowledge
* [ ] cpp/qt ipp server
  * [ ] implement basic server
  * [ ] implement stateless ipp printing
  * [ ] [uuid with cpp](https://stackoverflow.com/a/60198074) vs [qt uuid](https://doc.qt.io/qt-5/quuid.html)
  * [ ] implement status responses
* [ ] Find out if we can tell xochitl to update the file list without restarting
* [ ] learn about (and implement) IPP [authentication](https://manuals.ricoh.com/online/RICOH/wsmhlp/m003/en/rt0407.html), most likely via DIGEST
* Potential networking frameworks:
  * lgtm https://github.com/etr/libhttpserver
  * https://github.com/qt-labs/qthttpserver/blob/master/examples/httpserver/simple/main.cpp#L59 (qt cross compilation is what rm does and I can focus on IPP and don't have to worry about tcp & http)
  * https://github.com/sprinfall/webcc  (simple(r) cpp asio framework)
  * http://think-async.com/Asio/Download.html  (quite complex at the first glance)
  * https://github.com/chronoxor/CppServer (dependencies will likely cause me a headache during cross compilation)
  * apt install `moreutils` to query error numbers via `errno` (if working directly with [c sockets](https://ncona.com/2019/04/building-a-simple-server-with-cpp/))
* 
