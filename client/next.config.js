/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  alias: {
    // react: path.resolve('./node_modules/react')
  },
  compilerOptions: {
    checkJs: true
  }
}

module.exports = nextConfig
