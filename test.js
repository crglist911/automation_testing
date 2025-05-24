// Simple assertion function for testing
function assertEquals(actual, expected, testName) {
    if (actual === expected) {
        console.log(`PASSED: ${testName}`);
    } else {
        console.error(`FAILED: ${testName}`);
        console.error(`  Expected: "${expected}"`);
        console.error(`  Actual:   "${actual}"`);
    }
}

// Function to be tested (mirrors the logic in script.js)
function formatTypeToCssClass(typeString) {
    if (typeof typeString !== 'string') {
        return ''; // Or throw an error, depending on desired handling
    }
    return typeString.toLowerCase().replace(/ /g, '-');
}

// Test cases
assertEquals(formatTypeToCssClass("Noble Gas"), "noble-gas", "Test Noble Gas formatting");
assertEquals(formatTypeToCssClass("Alkali Metal"), "alkali-metal", "Test Alkali Metal formatting");
assertEquals(formatTypeToCssClass("Nonmetal"), "nonmetal", "Test Nonmetal formatting (single word)");
assertEquals(formatTypeToCssClass(""), "", "Test empty string formatting");
assertEquals(formatTypeToCssClass("Post-transition Metal"), "post-transition-metal", "Test string with hyphen formatting");

console.log("\nTo run these tests, open your browser's developer console and paste the content of this file, or run it with Node.js if you have it installed (node test.js).");
console.log("In a real project, you would use a testing framework like Jest or Mocha.");
