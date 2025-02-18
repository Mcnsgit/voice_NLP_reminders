from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from typing import Dict

import logging

logger = logging.getLogger(__name__)


class EndpointTester:
    """
    Utility class for testing and verifying API endpoints.
    Provides methods for common endpoint testing scenarios.
    """

    def __init__(self, client: TestClient):
        self.client = client
        self.test_task_data = None
        self.auth_headers = {"Authorization": "Bearer test_token"}

    async def verify_task_endpoints(self) -> Dict[str, bool]:
        """
        Verify all task-related endpoints are working correctly.
        Returns a dictionary of test results.
        """
        results = {}

        try:
            # Test task creation
            results["create_task"] = await self.test_create_task()

            # Test task retrieval
            results["get_tasks"] = await self.test_get_tasks()

            if self.test_task_data:
                # Test task detail retrieval
                results["get_task_detail"] = await self.test_get_task_detail()

                # Test task update
                results["update_task"] = await self.test_update_task()

                # Test task deletion
                results["delete_task"] = await self.test_delete_task()

            # Test task statistics
            results["get_statistics"] = await self.test_get_statistics()

        except Exception as e:
            logger.error(f"Error during endpoint testing: {str(e)}")
            results["error"] = str(e)

        return results

    async def test_create_task(self) -> bool:
        """Test task creation endpoint"""
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "priority": 2,
        }

        response = self.client.post(
            "/api/v1/tasks/", json=task_data, headers=self.auth_headers
        )

        if response.status_code == 200:
            self.test_task_data = response.json()
            return True

        logger.error(f"Task creation failed: {response.text}")
        return False

    async def test_get_tasks(self) -> bool:
        """Test task list retrieval endpoint"""
        response = self.client.get("/api/v1/tasks/", headers=self.auth_headers)

        if response.status_code != 200:
            logger.error(f"Get tasks failed: {response.text}")
            return False

        data = response.json()
        return all(key in data for key in ["items", "total", "page", "size", "pages"])

    async def test_get_task_detail(self) -> bool:
        """Test task detail retrieval endpoint"""
        if not self.test_task_data:
            return False

        response = self.client.get(
            f"/api/v1/tasks/{self.test_task_data['id']}", headers=self.auth_headers
        )

        if response.status_code != 200:
            logger.error(f"Get task detail failed: {response.text}")
            return False

        data = response.json()
        return all(
            key in data
            for key in ["id", "title", "description", "notes_count", "reminders_count"]
        )

    async def test_update_task(self) -> bool:
        """Test task update endpoint"""
        if not self.test_task_data:
            return False

        update_data = {"title": "Updated Test Task", "priority": 3}

        response = self.client.put(
            f"/api/v1/tasks/{self.test_task_data['id']}",
            json=update_data,
            headers=self.auth_headers,
        )

        if response.status_code != 200:
            logger.error(f"Update task failed: {response.text}")
            return False

        data = response.json()
        return data["title"] == update_data["title"]

    async def test_delete_task(self) -> bool:
        """Test task deletion endpoint"""
        if not self.test_task_data:
            return False

        response = self.client.delete(
            f"/api/v1/tasks/{self.test_task_data['id']}", headers=self.auth_headers
        )

        if response.status_code != 200:
            logger.error(f"Delete task failed: {response.text}")
            return False

        # Verify task is actually deleted
        get_response = self.client.get(
            f"/api/v1/tasks/{self.test_task_data['id']}", headers=self.auth_headers
        )

        return get_response.status_code == 404

    async def test_get_statistics(self) -> bool:
        """Test task statistics endpoint"""
        response = self.client.get(
            "/api/v1/tasks/statistics/summary", headers=self.auth_headers
        )

        if response.status_code != 200:
            logger.error(f"Get statistics failed: {response.text}")
            return False

        data = response.json()
        return all(
            key in data
            for key in [
                "total_tasks",
                "tasks_by_status",
                "overdue_tasks",
                "completion_rate",
            ]
        )

    def print_test_results(self, results: Dict[str, bool]) -> None:
        """Print test results in a readable format"""
        print("\nEndpoint Test Results:")
        print("-" * 50)
        for endpoint, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{endpoint:.<40} {status}")
        print("-" * 50)
