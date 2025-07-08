import { test, expect } from '@playwright/test';

test.describe('Draft E2E Tests', () => {
  test('should allow voter registration, run draft, and display results', async ({ page }) => {
    // 1. Open root, submit three choices for two voters.
    await page.goto('http://localhost:3000/');

    // Voter 1
    await page.fill('#email', 'voter1@example.com');
    await page.fill('#choice1', '1');
    await page.fill('#choice2', '2');
    await page.fill('#choice3', '3');
    await page.click('button:has-text("Register Voter")');
    await expect(page.locator('text=Voter registered successfully!')).toBeVisible();

    // Voter 2
    await page.fill('#email', 'voter2@example.com');
    await page.fill('#choice1', '4');
    await page.fill('#choice2', '5');
    await page.fill('#choice3', '6');
    await page.click('button:has-text("Register Voter")');
    await expect(page.locator('text=Voter registered successfully!')).toBeVisible();

    // 2. Call /draft/run via admin button.
    await page.click('button:has-text("Run Draft and View Round 1 Results")');
    await expect(page.locator('text=Draft run successfully!')).toBeVisible();

    // 3. Verify page /results/1 shows round1 winners table.
    await page.waitForURL('http://localhost:3000/results/1');
    await expect(page.locator('h1:has-text("Round 1 Results")')).toBeVisible();
    await expect(page.locator('text=voter1@example.com')).toBeVisible();
    await expect(page.locator('text=voter2@example.com')).toBeVisible();
    // Add more specific assertions for assigned lands if needed
  });
});
