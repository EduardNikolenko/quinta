# quinta
Minimalistic web framework

## Usage
```python
from quinta import Quinta

app = Quinta()

@app.route('/')
def home():
    print('Hallo world')

@app.route('/page')
def page():
    print('Is a page')

if __name__ == '__main__':
    app.run()
```

## License

MIT © [Eduard Nikolenko](https://github.com/eduardnikolenko)
