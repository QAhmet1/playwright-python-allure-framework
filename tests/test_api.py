import pytest
import allure


@allure.epic("Core API Services")
@allure.feature("Post Management Service")
class TestAPI:

    """
    EN: API Regression suite for Post service CRUD operations.
    """

    @allure.story("Get Operations")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Fetches a single post and validates the JSON schema fields.")
    def test_get_single_post_and_validate_schema(self, post_service):
        with allure.step("Request: GET single post with ID 1"):
            response = post_service.get_single_post(1)
            data = response.json()
        
        with allure.step("Verify response status code is 200"):
            assert response.status == 200
            
        with allure.step("Validate JSON schema keys and data types"):
            expected_keys = {"userId", "id", "title", "body"}
            assert expected_keys.issubset(data.keys()), f"Missing fields: {expected_keys - data.keys()}"
            assert isinstance(data["id"], int)


    @allure.story("Update Operations")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("new_title", ["Updated Title 1", "Elite Test Update"])
    def test_patch_post_title(self, post_service, new_title):
        allure.dynamic.title(f"Patch Post Title: {new_title}")
        
        with allure.step(f"Request: PATCH post title to '{new_title}'"):
            response = post_service.update_post_partial(1, new_title)
            
        with allure.step("Verify update was successful and title matches"):
            assert response.status == 200
            assert response.json()["title"] == new_title


        with allure.step("Request: GET post with non-existent ID 9999"):
            response = post_service.get_single_post(9999)
            
        with allure.step("Verify response status is 404"):
            assert response.status == 404

    @allure.story("Delete Operations")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verifies that a post can be deleted from the system.")
    def test_delete_and_verify(self, post_service):
        with allure.step("Request: DELETE post with ID 1"):
            response = post_service.delete_post(1)
            
        with allure.step("Verify deletion status code is 200"):
            assert response.status == 200