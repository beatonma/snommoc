export FILE_COMPOSE="compose.prod-demo.yml"
export FILE_ENV=".env.production"
export BUILD_TYPE="production"

POSTGRES_CONTAINER_NAME="snommoc_postgres"

usage="$(basename "$0") demo
  shell            Open a shell in the running Django container.
  export           Export database and media files to a backup archive.
  import FILE      Restore database and media files from a backup archive.
"

source ./tools/manage/common.sh

django_shell() {
  run_command docker exec -it snommoc_demo-django sh
  exit 0
}


run_action() {
  case "$1" in
    "shell")
      django_shell
      ;;
    "import")
      import_data "$POSTGRES_CONTAINER_NAME" "$2"
      ;;
    "export")
      export_data "$POSTGRES_CONTAINER_NAME"
      ;;
    *)
      log "$usage"
      ;;
  esac
  exit 0
}
export run_action
