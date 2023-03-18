#ifndef KB_LIB_KROMBLAST_H
#define KB_LIB_KROMBLAST_H

#include "kb_lib_core.hpp"
#include "kb_lib_class.hpp"
#include <string>
#include <functional>
#include <vector>

/**
 * @brief Namespace of the kromblast library
 * @class KromblastInterface Interface of the kromblast library
 */
namespace KromblastCore
{

    /**
     * @brief Interface of the kromblast library
     * @property kromblast_callback Callback of the library
     * @property set_html Set the html of the webview
     * @property navigate Navigate to a url
     * @property run Run the webview
     * @property is_debug Get the debug mode
     * @property log Log a message
     * @property get_version Get the kromblast version
     * @property claim_callback Claim a callback
     * @property get_functions Get the list of the callback functions
     */
    class KromblastInterface
    {
    public:
        /**
         * @brief Function called for each function
         * @param req Request
         * @return Return the result of the function
         */
        virtual const std::string kromblast_callback(const std::string req) = 0;

        /**
         * @brief Set the html of the webview
         * @param html Html
         */
        virtual void set_html(const std::string html) = 0;

        /**
         * @brief Navigate to a url
         * @param url Url
         */
        virtual void navigate(const std::string url) = 0;

        /**
         * @brief Run the webview
         */
        virtual void run() = 0;

        /**
         * @brief Get the debug mode
         */
        virtual bool is_debug() = 0;

        /**
         * @brief Log a message
         */
        virtual void log(const std::string lib, const std::string message) = 0;

        /**
         * @brief Get the kromblast version
         */
        virtual const std::string get_version() = 0;

        /**
         * @brief Claim a callback
         * @param callback Callback
         * @return Return true if the callback is claimed
         */
        virtual bool claim_callback(struct KromblastCore::kromblast_callback *callback) = 0;

        /**
         * @brief Get the functions
         * @return Return the functions
         */
        virtual std::vector<KromblastCore::kromblast_callback> get_functions() = 0;
    };
}
#endif