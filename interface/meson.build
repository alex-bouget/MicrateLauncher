project(
    'MicrateInterface',
    'cpp',
    version : '0.1',
    default_options : ['warning_level=3']
)


kromblast_api_dep = declare_dependency(
    include_directories : include_directories('src/include/'),
)

exe = shared_library(
    'MicrateInterface',
    'src/main.cpp',
    install : true,
    dependencies : kromblast_api_dep,
)
