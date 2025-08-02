export FILE_COMPOSE="compose.test.yml"
export FILE_ENV=".env.dev"
export BUILD_TYPE="test"

usage="$(basename "$0") test
  [default]        Run all unit tests from django and next.js
  jest             Run tests from next.js
  django           Run tests from django
"

source ./tools/manage/common.sh


jest() {
  docker_compose run --rm --entrypoint="npm run jest" jest
}
jestWatch() {
  docker_compose run --rm --entrypoint="npm run jest:watch" jest
}

django() {
  docker_compose run --rm --entrypoint="python -m pytest -rs $*" django
}

unittests() {
  jest
  django
}

run_action() {
  case "$1" in
    "-h" | "--help" | "?")
      log "$usage"
      ;;
    "django")
      shift
      django "$@"
      ;;
    "jest")
      jestWatch
      ;;
    *)
      unittests
      ;;
  esac
  exit 0
}
export run_action
