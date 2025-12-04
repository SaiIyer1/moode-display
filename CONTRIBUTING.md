# Contributing to Moode Audio Touchscreen Display

Thank you for your interest in contributing! This project welcomes contributions from everyone.

## How to Contribute

### Reporting Bugs

Found a bug? Please open an issue with:

1. **Clear title** - "Radio browser crashes when..." not "Bug"
2. **Description** - What happened vs what you expected
3. **Steps to reproduce**:
   - Step 1
   - Step 2
   - Bug appears
4. **Environment**:
   - Raspberry Pi model
   - Moode Audio version
   - Python version
   - Screen resolution
5. **Logs** - Include relevant logs:
   ```bash
   tail -50 /home/moodepi/display_debug.log
   ```

### Suggesting Features

Have an idea? Open an issue with:

1. **Clear description** - What feature you want
2. **Use case** - Why it would be useful
3. **Mock-up** - Sketch or description of UI (if applicable)
4. **Alternatives** - Other ways to achieve the same goal

### Pull Requests

Want to contribute code? Great!

#### Before You Start

1. **Check existing issues** - Someone might already be working on it
2. **Open an issue first** - Discuss your idea before coding
3. **Keep it focused** - One feature or fix per PR

#### Development Setup

```bash
# Fork the repository on GitHub

# Clone your fork
git clone https://github.com/YOUR_USERNAME/moode-display.git
cd moode-display

# Create a branch
git checkout -b feature/my-amazing-feature

# Make your changes
nano moode_display.py

# Test thoroughly
python3 moode_display.py

# Commit
git add moode_display.py
git commit -m "Add amazing feature"

# Push
git push origin feature/my-amazing-feature

# Open Pull Request on GitHub
```

#### Code Style

Follow existing code style:

**Python:**
- Use 4 spaces for indentation
- Follow PEP 8 generally
- Add comments for complex logic
- Use descriptive variable names

**Example:**
```python
def calculate_volume_step(current_volume, direction):
    """
    Calculate new volume based on current volume and direction.
    
    Args:
        current_volume: Current volume (0-100)
        direction: 'up' or 'down'
    
    Returns:
        New volume (0-100)
    """
    step = 5
    if direction == 'up':
        return min(100, current_volume + step)
    else:
        return max(0, current_volume - step)
```

#### Testing Checklist

Before submitting PR, test:

- [ ] Code runs without errors
- [ ] Syntax check passes: `python3 -m py_compile moode_display.py`
- [ ] Display starts correctly
- [ ] Touch controls work
- [ ] Radio browser works
- [ ] Doesn't break existing features
- [ ] Tested on actual hardware (if possible)
- [ ] Logs don't show errors

#### Documentation

Update documentation if needed:

- Add to README.md if user-facing feature
- Update CONFIGURATION.md if adding options
- Add to TROUBLESHOOTING.md if fixing common issue
- Update CHANGELOG.md

#### Commit Messages

Write clear commit messages:

**Good:**
```
Add volume step configuration option

- Add VOLUME_STEP constant
- Allow users to customize volume increment
- Update CONFIGURATION.md with new option
```

**Bad:**
```
fix bug
```

### First Time Contributors

New to open source? Welcome! Here are good first issues:

**Easy fixes:**
- Fix typos in documentation
- Add comments to code
- Improve error messages
- Add configuration examples

**Medium:**
- Add new color themes
- Improve button layouts
- Add keyboard shortcuts
- Optimize performance

**Advanced:**
- Add new features (favorites, search, etc.)
- Integrate with other services
- Add animations
- Multi-language support

## Code of Conduct

Be respectful and constructive:

- ✅ Be welcoming to newcomers
- ✅ Give constructive feedback
- ✅ Accept criticism gracefully
- ✅ Focus on what's best for the project
- ❌ No harassment or trolling
- ❌ No spam or off-topic content

## Questions?

- Open a Discussion on GitHub
- Ask in the Moode Audio forum
- Check existing Issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be listed in:
- GitHub contributors page (automatic)
- CHANGELOG.md (for significant contributions)
- README.md (for major features)

Thank you for contributing! 🎉
