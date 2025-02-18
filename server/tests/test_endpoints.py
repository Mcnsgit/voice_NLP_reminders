# app/tests/test_endpoints.py
import asyncio
import logging
from fastapi.testclient import TestClient
from main import app
from app.db.session import database_session
from app.core.config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from tests.endpoint_tester import EndpointTester

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Create test client
client = TestClient(app)


async def verify_database_connection(db: AsyncSession):
    """Verify database connection and create test user if needed"""
    try:
        await db.execute("SELECT 1")
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        return False


async def create_test_user(db: AsyncSession) -> User:
    """Create a test user for endpoint verification"""
    test_user = User(
        email="test@example.com",
        hashed_password="test_hash",
        is_active=True,
    )
    db.add(test_user)
    await db.commit()
    await db.refresh(test_user)
    return test_user


async def main():
    """Main testing function"""
    logger.info("\nStarting API Endpoint Verification")
    logger.info("=" * 50)

    # Establish database connection once
    async for db in database_session():
        # Verify database connection
        if not await verify_database_connection(db):
            logger.error(
                "❌ Cannot proceed with tests due to database connection failure"
            )
            return

        # Create test user if needed
        test_user = await create_test_user(db)

        tester = EndpointTester(client)

        # Set authentication for test user
        tester.auth_headers = {"Authorization": f"Bearer {test_user.id}"}

        # Run tests
        results = await tester.verify_task_endpoints()

        # Print results
        tester.print_test_results(results)

        # Print suggestions for any failures
        if not all(results.values()):
            logger.info("\nSuggestions for failed tests:")
            if not results.get("create_task"):
                logger.info("- Check task validation in TaskCreate schema")
                logger.info("- Verify database constraints")
            if not results.get("get_tasks"):
                logger.info("- Check pagination implementation")
                logger.info("- Verify task query filters")
            if not results.get("get_task_detail"):
                logger.info("- Verify task relationships (notes, reminders)")
            if not results.get("update_task"):
                logger.info("- Check permission validation")
                logger.info("- Verify task update logic")
            if not results.get("delete_task"):
                logger.info("- Check cascade deletion settings")
                logger.info("- Verify user ownership validation")
            if not results.get("get_statistics"):
                logger.info("- Check statistics calculation logic")
                logger.info("- Verify aggregation queries")


if __name__ == "__main__":
    asyncio.run(main())
