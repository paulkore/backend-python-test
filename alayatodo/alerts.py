from flask import flash


def alert(msg):
    alert_info(msg)


def alert_info(msg):
    flash(msg, 'alert-info')


def alert_success(msg):
    flash(msg, 'alert-success')


def alert_warning(msg):
    flash(msg, 'alert-warning')


def alert_error(msg):
    flash(msg, 'alert-danger')

