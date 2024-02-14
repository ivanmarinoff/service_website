# from django.test import TestCase
#
# # Create your tests here.
# import unittest
# from unittest.mock import Mock
# from Vehicle_service.admin_user.views import logout
#
#
# class TestLogout(unittest.TestCase):
#
#     def test_logout_post_request(self):
#         mock_request = Mock(method='POST')
#         mock_request.user = Mock(__class__=Mock())
#         mock_render = Mock()
#         with unittest.mock.patch('Vehicle_service.admin_user.views.user_logged_out') as mock_user_logged_out:
#             with unittest.mock.patch('Vehicle_service.admin_user.views.clear_session') as mock_clear_session:
#                 with unittest.mock.patch('Vehicle_service.admin_user.views.render',
#                                          return_value=mock_render) as mock_render:
#                     logout(mock_request)
#                     mock_user_logged_out.assert_called_once_with(sender=mock_request.user.__class__,
#                                                                  request=mock_request, user=mock_request.user)
#                     mock_clear_session.assert_called_once_with(mock_request)
#                     mock_render.assert_called_once_with(mock_request, 'vehicle/index.html')
#
#     def test_logout_non_post_request(self):
#         mock_request = Mock(method='GET')
#         mock_render = Mock()
#         with unittest.mock.patch('Vehicle_service.admin_user.views.render', return_value=mock_render) as mock_render:
#             result = logout(mock_request)
#             mock_render.assert_called_once_with(mock_request, 'vehicle/index.html')
#             self.assertEqual(result, mock_render.return_value)
#
#
# if __name__ == '__main__':
#     unittest.main()
