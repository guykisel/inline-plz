module.exports = {
  // Prevent parent eslintrc from interfering
  "root": true,

  // Begin with the recommended rules from eslint itself
  "extends": "eslint:recommended",

  // Globals
  "env": {
    "browser": true,
    "node": true,
    "es6": true
  },

  // ES6
  "parserOptions": {
    "ecmaVersion": 6,
    "sourceType": "module"
  },

  "rules": {
    // Disallow declaring the same variable more then once
    //
    // Reasons: stylistic, gotcha
    // See http://eslint.org/docs/rules/no-redeclare.html
    "no-redeclare": 2,

    // Disallow the declaration of duplicate keys in an object
    //
    // Reasons: safety, gotcha
    // See http://eslint.org/docs/rules/no-dupe-keys.html
    "no-dupe-keys": 2,

    // Disallow use of undeclared variables unless mentioned in a /*global */ block
    //
    // Reasons: side-effects, safety
    // See http://eslint.org/docs/rules/no-undef.html
    "no-undef": 2,

    // Enforce camelCase names, but allow snake_case
    // properties on objects where necessary.
    //
    // Best practice recommendation is camelCase always.
    //
    // Reasons: stylistic
    // See http://eslint.org/docs/rules/camelcase
    "camelcase" : [2, {"properties": "never"}],

    // Require use of === and !== to avoid problematic
    // type coercion
    //
    // Reasons: safety, gotcha
    // See http://eslint.org/docs/rules/eqeqeq
    "eqeqeq": 2,

    // Require valid JSDoc comments, where JSDoc comments
    // are used. You are free to not document functions,
    // but when functions are documented (like your public API -
    // you document that, right?) the JSDoc comments must be
    // valid and match the params of the given function.
    //
    // Reasons: maintainability, readability
    // See http://usejsdoc.org/
    // See http://eslint.org/docs/rules/valid-jsdoc
    "valid-jsdoc": [2, {
      "requireParamDescription": true,
      "requireReturnDescription": true,
      "requireReturn": true
    }],

    // Require curly braces for every new block or
    // scope, including single-line statements.
    //
    // Reasons: safety, stylistic, readability
    // See http://eslint.org/docs/rules/curly
    "curly" : 2,

    // Prevent extension of built-in objects.
    //
    // Reasons: side-effects, safety
    // See http://eslint.org/docs/rules/no-extend-native
    "no-extend-native": 2,

    // Prevent reassignment/shadowing of native objects
    //
    // Reasons: side-effects, safety
    // See http://eslint.org/docs/rules/no-native-reassign
    "no-native-reassign": 2,

    // Require indentation in line with most idiomatic
    // Javascript style guides: two spaces, no tabs
    //
    // Reasons: stylistic, consistency
    // See http://eslint.org/docs/rules/indent
    "indent" : [2, 2], // {int} Number of spaces to use for indentation

    // Require that `new`-able objects are represented
    // by a symbol with a capital letter
    //
    // Reasons: stylistic
    // See http://eslint.org/docs/rules/new-cap
    "new-cap" : 2, // true: Require capitalization of all constructor functions e.g. `new F()`

    // Require that parentheses are used when `new`-ing a
    // constructor, even if the constructor has no arguments.
    //
    // Reasons: stylistic
    // See http://eslint.org/docs/rules/new-parens
    "new-parens": 2,

    // Forbid use of `new` without assigning the result
    //
    // Reasons: side-effects
    // See http://eslint.org/docs/rules/no-new
    "no-new" : 2,

    // Prevent inclusion of unused variables in final code
    //
    // Reasons: maintainability
    // See http://eslint.org/docs/rules/no-unused-vars
    "no-unused-vars": 2,

    // Fail on finding lines with trailing whitespace.
    // Indicates that you may have a misconfigured text editor.
    //
    // Reasons: stylistic
    // See http://eslint.org/docs/rules/no-trailing-spaces
    "no-trailing-spaces": 2,

    // Limit arity of functions. While you may occasionally
    // need to create a function with higher arity than recommended,
    // these functions should be marked as exceptions with linter
    // comments.
    //
    // Reasons: maintainability
    // See http://eslint.org/docs/rules/max-params
    "max-params" : [2, 5],

    // Limit block-depth of code for management of complexity
    //
    // Reasons: readability, maintainability
    // See http://eslint.org/docs/rules/max-depth
    "max-depth" : [2, 4],

    // Avoid nested callbacks wherever possible. Prefer
    // promises over nesting.
    //
    // Reasons: readability, maintainability
    // See http://eslint.org/docs/rules/max-nested-callbacks
    "max-nested-callbacks": [2, 3],

    // Limit length of functions - prefer small units of
    // functionality over long routines
    //
    // Reasons: readability, maintainability
    // See http://eslint.org/docs/rules/max-statements
    "max-statements" : [2, 20],

    // Limit cyclomatic complexity
    //
    // Reasons: readability, maintainability
    // See http://eslint.org/docs/rules/complexity
    "complexity" : [2, 5],

    // Limit line lengths
    //
    // Reasons: readability
    // http://eslint.org/docs/rules/max-len
    "max-len" : [2, 120],

    // Prevent mixed spaces and tabs
    //
    // Reasons: stylistic
    // See http://eslint.org/docs/rules/no-mixed-spaces-and-tabs
    "no-mixed-spaces-and-tabs": [2, true],

    // Require space after:
    // if, else, for, while, do, switch, try, catch, finally, and with.
    //
    // Reasons: readability, stylistic
    // See http://eslint.org/docs/rules/keyword-spacing
    "keyword-spacing": [2],

    // Require spaces around operators
    //
    // Reasons: readability, stylistic
    // See http://eslint.org/docs/rules/space-infix-ops
    "space-infix-ops": 2,

    // Forbid spaces between function name and parens when calling
    //
    // Reasons: readability, stylistic
    // See http://eslint.org/docs/rules/no-spaced-func
    "no-spaced-func": 2,

    // Require commas at end of line, never start
    //
    // Reasons: readability, stylistic
    // See http://eslint.org/docs/rules/comma-style
    "comma-style": [2, "last"],

    // Require linefeed at end of file
    //
    // Reasons: scripting/concat compatibility
    // See http://eslint.org/docs/rules/eol-last
    "eol-last": 2,

    // Use 'self' as replacement for 'this' where necessary
    //
    // Reasons: readability, stylistic
    // See http://eslint.org/docs/rules/consistent-this
    "consistent-this": [2, "self"],

    // Require no space between function and open parenthsis
    //
    // Reasons: readability, stylistic
    // See http://eslint.org/docs/rules/space-before-function-paren
    "space-before-function-paren": [2, "never"],

    // Braces should start on the same line as the corresponidng
    // statement or decleration.
    //
    // Reason: readability, stylistic
    // See http://eslint.org/docs/rules/brace-style
    "brace-style": [2, "1tbs", { "allowSingleLine": true }],

    // Require space before blocks
    //
    // Reason: readability, stylistic
    // See: http://eslint.org/docs/rules/space-before-blocks
    "space-before-blocks": [2, { "functions": "always", "keywords": "always", "classes": "always" }],

    // Disallow spaces directly after '(' and before ')'
    //
    // Reason: readability, stylistic
    // See http://eslint.org/docs/rules/space-in-parens
    "space-in-parens": [2, "never"],

    // Disallow spaces inside of curly braces in objects
    //
    // Reason: stylistic
    // See http://eslint.org/docs/rules/object-curly-spacing
    "object-curly-spacing": [2, "never"],

    // Disallow spaces inside of computed properties
    //
    // Reason: stylistic
    // See http://eslint.org/docs/rules/computed-property-spacing
    "computed-property-spacing": [2, "never"],

    // Disallow spaces inside of brackets
    //
    // Reason: stylistic
    // See http://eslint.org/docs/rules/array-bracket-spacing
    "array-bracket-spacing": [2, "never"],

    // Disallow space before comma and require space after comma
    //
    // Reason: readability, stylistic
    // See http://eslint.org/docs/rules/comma-spacing
    "comma-spacing": [2, {"before": false, "after": true}],

    // Disallow space before semicolon and require space after semicolon
    //
    // Reason: readability, stylistic
    // http://eslint.org/docs/rules/semi-spacing
     "semi-spacing": [2, {"before": false, "after": true}],

     "no-console": "warn"
  }

}
