# coding ~utf-8
"""

Author: Louai KB

Main application

"""


from view import View


if __name__ == '__main__':

    main_object = View()
    main_object.setup_main_interface()
    main_object.create_buttons()
    main_object.main_loop()