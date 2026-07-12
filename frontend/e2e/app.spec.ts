import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/FootGolf/);
});

test('can navigate to login', async ({ page }) => {
  await page.goto('/login');
  await expect(page.locator('h2')).toContainText('FootGolf Score');
});
