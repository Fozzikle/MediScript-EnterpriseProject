from File_Config import is_setup_completed
from loading_bar_def import run_loading

# Determines if ui or setup wizard opens depending on if they have used program before
if is_setup_completed():
    def ui_launch():
        run_loading(
            task_func=lambda: __import__('UI'),
            next_func=lambda: __import__('UI').UI_window()
        )


    ui_launch()


else:
    def buffer():
        pass


    def launch_setup():
        import Setup_Wizard
        Setup_Wizard.run_setup_wizard()
        Setup_Wizard.finish_setup()


    run_loading(task_func=buffer(), next_func=launch_setup())
