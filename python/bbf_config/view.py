# -*- coding: utf-8 -*-

import os

from PySide import QtGui

import tank

from ui.choose_config import Ui_Form
import core
import constants


class ChooseConfigDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(ChooseConfigDialog, self).__init__(parent)
        self._ui = Ui_Form()
        self._ui.setupUi(self)
        self._app = tank.platform.current_bundle()
        self._engine = self._app.engine
        self._project_id = self._app.context.project.get("id")
        framework_sgutils = self._app.frameworks.get("tk-framework-shotgunutils")
        settings_module = framework_sgutils.import_module("settings")
        self._settings_manager = settings_module.UserSettings(self._engine)

        self._populate_fields()
        self._init_signals()

    def _populate_fields(self):
        self._ui.config_combobox.addItems(core.get_all_override_configs())
        # config_file = self._settings_manager.retrieve("bbf_config_file_%s" % self._project_id, "primary.yml",
        #                                               self._settings_manager.SCOPE_PROJECT)
        config_file = core.get_config_file_name(self._project_id)
        self._ui.config_combobox.setCurrentIndex(self._ui.config_combobox.findText(config_file))
        self.on_change_config_combobox(config_file)

    def _init_signals(self):
        self._ui.go_btn.clicked.connect(self.on_click_go_btn)
        self._ui.config_combobox.currentIndexChanged[str].connect(self.on_change_config_combobox)

    def on_click_go_btn(self):
        self.close()

    def on_change_config_combobox(self, config_file_name):

        config_data = core.get_available_override_config(config_file_name)
        config_file_path = core.get_config_full_path(config_file_name)
        repo_config = config_data.get("bbf_localrepos_config") or {}
        local_repo_path = repo_config.get("local_url")
        remote_url = repo_config.get("remote_url")

        config_map = {
            self._ui.config_path_lbl: config_file_path or "--",
            self._ui.repo_path_lbl: local_repo_path or "--",
            self._ui.remote_lbl: remote_url or "--"
        }
        for lbl_widget, value in config_map.iteritems():
            lbl_widget.setText(value)

        # self._settings_manager.store("bbf_config_file_%s" % self._project_id, config_file_name,
        #                              self._settings_manager.SCOPE_PROJECT)

        core.store_config_file_name(self._project_id, config_file_name)


def show_choose_config_dialog(app_instance):
    app_instance.engine.show_dialog(constants.APP_NAME, app_instance, ChooseConfigDialog)

