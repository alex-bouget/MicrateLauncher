#ifndef KB_LIB_CORE_H
#define KB_LIB_CORE_H

#include <string>
#include <vector>
#include <functional>

/**
 * @brief Namespace of the kromblast library
 * @struct kromblast_callback_called Structure used to call a function
 * @typedef kromblast_callback_t Function type for a callback
 * @struct kromblast_callback Structure for simulating a function
 */
namespace KromblastCore
{
    /**
     * @brief Structure used to call a function
     * @property name Function name
     * @property args Arguments
     */
    struct kromblast_callback_called
    {
        std::string name;
        std::vector<std::string> args;
    };

    /**
     * @brief Structure for simulating a function
     * @property name Function name
     * @property args_nb Arguments number
     * @property callback Callback of the function
     */
    struct kromblast_callback
    {
        std::string name;
        int args_nb;
        std::function<std::string(struct KromblastCore::kromblast_callback_called *)> callback;
    };
}
#endif